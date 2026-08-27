const state = {
    devices: [],
    selectedDeviceId: null,
};

const elements = {
    deviceCount: document.querySelector("#device-count"),
    activeDeviceCount: document.querySelector("#active-device-count"),
    alertCount: document.querySelector("#alert-count"),
    devicesBody: document.querySelector("#devices-body"),
    deviceSelect: document.querySelector("#device-select"),
    readingValue: document.querySelector("#reading-value"),
    readingForm: document.querySelector("#reading-form"),
    selectedUnit: document.querySelector("#selected-unit"),
    selectedDeviceDetails: document.querySelector(
        "#selected-device-details"
    ),
    readingsBody: document.querySelector("#readings-body"),
    alertsList: document.querySelector("#alerts-list"),
    refreshButton: document.querySelector("#refresh-button"),
    message: document.querySelector("#message"),
};

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
        ...options,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        let errorMessage = `Request failed with status ${response.status}`;

        if (errorData?.detail) {
            if (Array.isArray(errorData.detail)) {
                errorMessage = errorData.detail
                    .map((error) => error.msg)
                    .join(", ");
            } else {
                errorMessage = errorData.detail;
            }
        }

        throw new Error(errorMessage);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

function showMessage(text, type = "success") {
    elements.message.textContent = text;
    elements.message.className = `message message-${type}`;
    elements.message.hidden = false;

    window.setTimeout(() => {
        elements.message.hidden = true;
    }, 5000);
}

function formatDate(timestamp) {
    if (!timestamp) {
        return "—";
    }

    return new Date(timestamp).toLocaleString();
}

function formatRange(device) {
    if (
        device.normal_min === null ||
        device.normal_min === undefined ||
        device.normal_max === null ||
        device.normal_max === undefined
    ) {
        return "Not configured";
    }

    return `${device.normal_min} – ${device.normal_max} ${device.unit}`;
}

function createTableCell(text) {
    const cell = document.createElement("td");
    cell.textContent = text;
    return cell;
}

function getSelectedDevice() {
    return state.devices.find(
        (device) => device.id === state.selectedDeviceId
    );
}

function renderDeviceSummary() {
    elements.deviceCount.textContent = state.devices.length;

    const activeCount = state.devices.filter(
        (device) => device.status === "active"
    ).length;

    elements.activeDeviceCount.textContent = activeCount;
}

function renderDevices() {
    elements.devicesBody.replaceChildren();

    if (state.devices.length === 0) {
        const row = document.createElement("tr");
        const cell = createTableCell("No devices have been created.");
        cell.colSpan = 5;
        cell.className = "empty-state";
        row.appendChild(cell);
        elements.devicesBody.appendChild(row);
        return;
    }

    state.devices.forEach((device) => {
        const row = document.createElement("tr");
        row.className = "device-row";

        if (device.id === state.selectedDeviceId) {
            row.classList.add("selected-row");
        }

        row.appendChild(createTableCell(device.name));
        row.appendChild(createTableCell(device.type));

        const statusCell = document.createElement("td");
        const statusBadge = document.createElement("span");

        statusBadge.className =
            `status-badge status-${device.status}`;
        statusBadge.textContent = device.status;

        statusCell.appendChild(statusBadge);
        row.appendChild(statusCell);

        row.appendChild(createTableCell(device.unit));
        row.appendChild(createTableCell(formatRange(device)));

        row.addEventListener("click", () => {
            selectDevice(device.id);
        });

        elements.devicesBody.appendChild(row);
    });
}

function populateDeviceSelect() {
    elements.deviceSelect.replaceChildren();

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select a device";
    elements.deviceSelect.appendChild(defaultOption);

    state.devices.forEach((device) => {
        const option = document.createElement("option");
        option.value = device.id;
        option.textContent = `${device.name} (${device.status})`;
        elements.deviceSelect.appendChild(option);
    });

    elements.deviceSelect.value = state.selectedDeviceId ?? "";
}

function updateSelectedDeviceDetails() {
    const device = getSelectedDevice();
    const submitButton = elements.readingForm.querySelector(
        "button[type='submit']"
    );

    if (!device) {
        elements.selectedUnit.textContent = "—";
        elements.selectedDeviceDetails.textContent =
            "Select a device to view its recent readings.";
        elements.readingValue.disabled = true;
        submitButton.disabled = true;
        return;
    }

    elements.selectedUnit.textContent = device.unit;

    elements.selectedDeviceDetails.textContent =
        `${device.name} · ${device.type} · ` +
        `Normal range: ${formatRange(device)}`;

    const isInactive = device.status !== "active";

    elements.readingValue.disabled = isInactive;
    submitButton.disabled = isInactive;

    submitButton.textContent = isInactive
        ? "Device Inactive"
        : "Submit Reading";
}

async function loadReadings() {
    if (!state.selectedDeviceId) {
        elements.readingsBody.replaceChildren();

        const row = document.createElement("tr");
        const cell = createTableCell("No device selected.");
        cell.colSpan = 3;
        cell.className = "empty-state";

        row.appendChild(cell);
        elements.readingsBody.appendChild(row);
        return;
    }

    elements.readingsBody.replaceChildren();

    const loadingRow = document.createElement("tr");
    const loadingCell = createTableCell("Loading readings...");
    loadingCell.colSpan = 3;
    loadingCell.className = "empty-state";
    loadingRow.appendChild(loadingCell);
    elements.readingsBody.appendChild(loadingRow);

    try {
        const readings = await apiRequest(
            `/api/devices/${state.selectedDeviceId}/readings?limit=20`
        );

        elements.readingsBody.replaceChildren();

        if (readings.length === 0) {
            const row = document.createElement("tr");
            const cell = createTableCell(
                "No readings found for this device."
            );

            cell.colSpan = 3;
            cell.className = "empty-state";
            row.appendChild(cell);
            elements.readingsBody.appendChild(row);
            return;
        }

        readings.forEach((reading) => {
            const row = document.createElement("tr");

            row.appendChild(createTableCell(reading.value));
            row.appendChild(createTableCell(reading.unit));
            row.appendChild(
                createTableCell(formatDate(reading.timestamp))
            );

            elements.readingsBody.appendChild(row);
        });
    } catch (error) {
        elements.readingsBody.replaceChildren();

        const row = document.createElement("tr");
        const cell = createTableCell(error.message);

        cell.colSpan = 3;
        cell.className = "empty-state";
        row.appendChild(cell);
        elements.readingsBody.appendChild(row);

        showMessage(error.message, "error");
    }
}

function renderAlerts(alerts) {
    elements.alertsList.replaceChildren();
    elements.alertCount.textContent = alerts.length;

    if (alerts.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "empty-state";
        emptyMessage.textContent = "There are no active alerts.";
        elements.alertsList.appendChild(emptyMessage);
        return;
    }

    alerts.forEach((alert) => {
        const device = state.devices.find(
            (item) => item.id === alert.device_id
        );

        const card = document.createElement("article");
        card.className = "alert-card";

        const message = document.createElement("p");
        message.textContent = alert.message;

        const metadata = document.createElement("div");
        metadata.className = "alert-meta";

        const deviceName = document.createElement("span");
        deviceName.textContent =
            `Device: ${device?.name ?? alert.device_id}`;

        const value = document.createElement("span");
        const triggerValue =
            alert.trigger_value ?? alert.value ?? "—";

        value.textContent =
            `Reading: ${triggerValue} ${alert.unit ?? ""}`;

        const timestamp = document.createElement("span");
        timestamp.textContent =
            `Time: ${formatDate(alert.timestamp)}`;

        metadata.append(deviceName, value, timestamp);

        const resolveButton = document.createElement("button");
        resolveButton.type = "button";
        resolveButton.className = "resolve-button";
        resolveButton.textContent = "Resolve Alert";

        resolveButton.addEventListener("click", () => {
            resolveAlert(alert.id, resolveButton);
        });

        card.append(message, metadata, resolveButton);
        elements.alertsList.appendChild(card);
    });
}

async function selectDevice(deviceId) {
    state.selectedDeviceId = deviceId || null;

    elements.deviceSelect.value = state.selectedDeviceId ?? "";

    renderDevices();
    updateSelectedDeviceDetails();
    await loadReadings();
}

async function resolveAlert(alertId, button) {
    button.disabled = true;
    button.textContent = "Resolving...";

    try {
        await apiRequest(`/api/alerts/${alertId}/resolve`, {
            method: "PATCH",
        });

        showMessage("Alert resolved successfully.");
        await loadDashboard();
    } catch (error) {
        showMessage(error.message, "error");
        button.disabled = false;
        button.textContent = "Resolve Alert";
    }
}

async function submitReading(event) {
    event.preventDefault();

    const device = getSelectedDevice();

    if (!device) {
        showMessage("Please select a device.", "error");
        return;
    }

    const readingValue = Number(elements.readingValue.value);
    const submitButton = elements.readingForm.querySelector(
        "button[type='submit']"
    );

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    try {
        const result = await apiRequest(
            `/api/devices/${device.id}/readings`,
            {
                method: "POST",
                body: JSON.stringify({
                    value: readingValue,
                    unit: device.unit,
                    timestamp: new Date().toISOString(),
                }),
            }
        );

        elements.readingValue.value = "";

        if (result.alert) {
            showMessage(
                "Reading saved. An alert was created because it is outside the normal range."
            );
        } else {
            showMessage("Reading saved successfully.");
        }

        await loadDashboard();
    } catch (error) {
        showMessage(error.message, "error");
    } finally {
        updateSelectedDeviceDetails();
    }
}

async function loadDashboard() {
    elements.refreshButton.disabled = true;
    elements.refreshButton.textContent = "Refreshing...";

    try {
        const [devices, alerts] = await Promise.all([
            apiRequest("/api/devices"),
            apiRequest("/api/alerts?resolved=false"),
        ]);

        state.devices = devices;

        const selectedDeviceStillExists = state.devices.some(
            (device) => device.id === state.selectedDeviceId
        );

        if (!selectedDeviceStillExists) {
            state.selectedDeviceId =
                state.devices.length > 0
                    ? state.devices[0].id
                    : null;
        }

        renderDeviceSummary();
        renderDevices();
        populateDeviceSelect();
        updateSelectedDeviceDetails();
        renderAlerts(alerts);
        await loadReadings();
    } catch (error) {
        showMessage(error.message, "error");
    } finally {
        elements.refreshButton.disabled = false;
        elements.refreshButton.textContent = "Refresh Dashboard";
    }
}

elements.deviceSelect.addEventListener("change", (event) => {
    selectDevice(event.target.value);
});

elements.readingForm.addEventListener("submit", submitReading);

elements.refreshButton.addEventListener("click", loadDashboard);

loadDashboard();