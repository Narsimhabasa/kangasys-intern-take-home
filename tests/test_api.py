from typing import Any

from fastapi.testclient import TestClient


ACTIVE_DEVICE: dict[str, Any] = {
    "name": "Chiller Room Temperature Sensor",
    "type": "temperature-sensor",
    "status": "active",
    "unit": "C",
    "normal_min": 2,
    "normal_max": 8,
}


def create_device(
    client: TestClient,
    **changes: Any,
) -> dict[str, Any]:
    payload = ACTIVE_DEVICE | changes
    response = client.post("/api/devices", json=payload)

    assert response.status_code == 201

    return response.json()


def test_device_crud(client: TestClient) -> None:
    device = create_device(client)
    device_id = device["id"]

    get_response = client.get(f"/api/devices/{device_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == ACTIVE_DEVICE["name"]

    list_response = client.get("/api/devices")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_payload = {
        **ACTIVE_DEVICE,
        "name": "Updated Chiller Sensor",
        "normal_max": 9,
    }
    update_response = client.put(
        f"/api/devices/{device_id}",
        json=update_payload,
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Chiller Sensor"
    assert update_response.json()["normal_max"] == 9

    delete_response = client.delete(f"/api/devices/{device_id}")
    assert delete_response.status_code == 200

    missing_response = client.get(f"/api/devices/{device_id}")
    assert missing_response.status_code == 404


def test_normal_reading_does_not_create_alert(
    client: TestClient,
) -> None:
    device = create_device(client)

    response = client.post(
        f"/api/devices/{device['id']}/readings",
        json={
            "value": 4.1,
            "unit": "C",
            "timestamp": "2026-08-10T08:00:00Z",
        },
    )

    assert response.status_code == 201
    assert response.json()["alert"] is None

    alerts_response = client.get("/api/alerts")
    assert alerts_response.status_code == 200
    assert alerts_response.json() == []


def test_abnormal_reading_creates_and_resolves_alert(
    client: TestClient,
) -> None:
    device = create_device(client)

    reading_response = client.post(
        f"/api/devices/{device['id']}/readings",
        json={
            "value": 11.6,
            "unit": "C",
            "timestamp": "2026-08-10T08:45:00Z",
        },
    )

    assert reading_response.status_code == 201

    alert = reading_response.json()["alert"]
    assert alert is not None
    assert alert["trigger_value"] == 11.6
    assert alert["resolved"] is False
    assert "above" in alert["message"]

    resolve_response = client.patch(
        f"/api/alerts/{alert['id']}/resolve"
    )
    assert resolve_response.status_code == 200
    assert resolve_response.json()["resolved"] is True
    assert resolve_response.json()["resolved_at"] is not None

    active_alerts = client.get("/api/alerts")
    assert active_alerts.status_code == 200
    assert active_alerts.json() == []

    resolved_alerts = client.get(
        "/api/alerts",
        params={"resolved": "true"},
    )
    assert resolved_alerts.status_code == 200
    assert len(resolved_alerts.json()) == 1


def test_inactive_device_cannot_accept_readings(
    client: TestClient,
) -> None:
    device = create_device(
        client,
        status="inactive",
        normal_min=None,
        normal_max=None,
    )

    response = client.post(
        f"/api/devices/{device['id']}/readings",
        json={
            "value": 4.1,
            "unit": "C",
            "timestamp": "2026-08-10T08:00:00Z",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Inactive devices cannot accept readings"
    )


def test_reading_unit_must_match_device(
    client: TestClient,
) -> None:
    device = create_device(client)

    response = client.post(
        f"/api/devices/{device['id']}/readings",
        json={
            "value": 4.1,
            "unit": "F",
            "timestamp": "2026-08-10T08:00:00Z",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Reading unit must be 'C'"


def test_readings_can_be_filtered_by_start_time(
    client: TestClient,
) -> None:
    device = create_device(client)
    endpoint = f"/api/devices/{device['id']}/readings"

    client.post(
        endpoint,
        json={
            "value": 4.0,
            "unit": "C",
            "timestamp": "2026-08-10T08:00:00Z",
        },
    )
    client.post(
        endpoint,
        json={
            "value": 5.0,
            "unit": "C",
            "timestamp": "2026-08-10T09:00:00Z",
        },
    )

    response = client.get(
        endpoint,
        params={"start_time": "2026-08-10T08:30:00Z"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["value"] == 5.0


def test_reading_timestamp_is_returned_as_utc(
    client: TestClient,
) -> None:
    device = create_device(client)

    response = client.post(
        f"/api/devices/{device['id']}/readings",
        json={
            "value": 4.0,
            "unit": "C",
            "timestamp": "2026-08-28T12:00:00+05:30",
        },
    )

    assert response.status_code == 201
    assert response.json()["reading"]["timestamp"] == (
        "2026-08-28T06:30:00Z"
    )


def test_reading_filter_requires_timezone(
    client: TestClient,
) -> None:
    device = create_device(client)

    response = client.get(
        f"/api/devices/{device['id']}/readings",
        params={
            "start_time": "2026-08-28T00:00:00",
            "end_time": "2026-08-29T00:00:00Z",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "start_time must include a timezone"
    )