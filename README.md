# KangaSys Device Monitoring Service

A small full-stack application for managing physical devices, storing their readings, detecting abnormal values, and resolving alerts.

The project was developed as part of the KangaSys Software Engineering Intern take-home assignment.

## Features

### Device Management

- Create, list, view, update, and delete devices
- Supported device types:
  - Temperature sensor
  - Pressure gauge
  - Humidity sensor
  - Energy meter
  - Contact sensor
- Mark devices as active or inactive
- Configure a minimum and maximum normal range for each active device

### Reading Management

- Submit timestamped readings for a device
- View recent device readings
- Filter readings using start and end timestamps
- Reject readings for inactive devices
- Validate that the submitted unit matches the device unit

### Anomaly Detection

- Every new reading is compared with the device's configured normal range
- Values on the minimum or maximum boundary are considered normal
- Values below the minimum or above the maximum generate an alert
- Alerts store the triggering reading, value, unit, timestamp, and message
- Active alerts can be viewed and marked as resolved

### Dashboard

The single-page dashboard allows users to:

- View total and active device counts
- View device status and configured normal range
- Select a device and view its recent readings
- Submit a new reading
- View active alerts
- Resolve alerts
- Refresh dashboard data

Interactive API documentation is also available through FastAPI Swagger UI.

## Technology Stack

- **Backend:** Python, FastAPI
- **Database:** SQLite, SQLAlchemy
- **Validation:** Pydantic
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest, FastAPI TestClient
- **Version Control:** Git and GitHub

## Project Structure

```text
kangasys-intern-take-home/
├── .ai/
│   └── plan.md
├── app/
│   ├── routers/
│   │   ├── alerts.py
│   │   ├── devices.py
│   │   └── readings.py
│   ├── services/
│   │   └── anomaly.py
│   ├── static/
│   │   ├── app.js
│   │   ├── index.html
│   │   └── styles.css
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── sample-data/
├── tests/
│   ├── conftest.py
│   ├── test_anomaly.py
│   └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Narsimhabasa/kangasys-intern-take-home.git
cd kangasys-intern-take-home
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m uvicorn app.main:app --reload
```

### 5. Open the application

Dashboard:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

The SQLite database and its tables are created automatically when the application starts.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/devices` | Create a device |
| GET | `/api/devices` | List devices |
| GET | `/api/devices/{device_id}` | Get one device |
| PUT | `/api/devices/{device_id}` | Update a device |
| DELETE | `/api/devices/{device_id}` | Delete a device |
| POST | `/api/devices/{device_id}/readings` | Submit a reading |
| GET | `/api/devices/{device_id}/readings` | List and filter readings |
| GET | `/api/alerts` | List alerts |
| PATCH | `/api/alerts/{alert_id}/resolve` | Resolve an alert |
| GET | `/health` | Check application health |

Device listing supports `status` and `type` query filters.

Reading listing supports `start_time`, `end_time`, and `limit` query parameters.

Alert listing supports `resolved` and `device_id` query filters.

## Running the Tests

Run the complete test suite with:

```bash
python -m pytest -v
```

The test suite covers:

- Normal readings
- Minimum and maximum boundary readings
- Values below and above the normal range
- Invalid threshold ranges
- Device CRUD operations
- Automatic alert creation
- Alert resolution
- Inactive-device business rules
- Unit validation
- Reading time-range filtering

Current result:

```text
12 passed
```

## Design Decisions

### Per-device normal ranges

Normal ranges are stored on each device rather than globally on the device type.

The sample data contains two temperature sensors with different safe ranges. A chiller temperature sensor may require `2–8 °C`, while a server-room sensor may require `18–27 °C`. Per-device configuration supports this difference.

### Immediate alert creation

Every out-of-range reading creates an alert immediately. This rule is simple, deterministic, and easy to test.

In a production system, this could be extended with sustained-anomaly detection, alert deduplication, severity levels, or notification cooldown periods.

### Boundary handling

A reading equal to the configured minimum or maximum is normal. Only values strictly below the minimum or above the maximum create alerts.

### Inactive devices

Inactive devices cannot accept new readings. They may exist without a configured normal range.

### Unit consistency

A submitted reading must use the same unit configured for its device. This prevents values with incompatible units from being compared against the same threshold.

### Separation of concerns

- Routers handle HTTP requests and responses
- Pydantic schemas validate API data
- SQLAlchemy models manage persistence
- The anomaly service contains threshold business logic
- The frontend communicates with the backend through REST endpoints

The anomaly detector is implemented as a separate, pure service so it can be tested independently and extended without changing the API layer.

## Assumptions

- Device types come from a small fixed list
- Active devices require minimum and maximum thresholds
- Each out-of-range reading creates one alert
- Timestamps are stored and exchanged in UTC
- Resolving an alert does not delete it
- Deleting a device also removes its associated readings and alerts

## Trade-offs and Future Improvements

SQLite was selected because it is lightweight and appropriate for a self-contained assignment. A production version would likely use PostgreSQL and database migrations.

Given more time, I would add:

- Authentication and authorization
- PostgreSQL and Alembic migrations
- Pagination for devices, readings, and alerts
- Sustained-anomaly and alert-deduplication rules
- Device creation and editing forms in the dashboard
- Charts for historical readings
- Structured logging and monitoring
- Docker support
- Continuous integration using GitHub Actions
- Cloud deployment

## AI-Assisted Workflow

AI tools were used iteratively to help with planning, code structure, test-case suggestions, and debugging. The implementation was divided into separate commits instead of being generated as a single one-shot solution.

The initial implementation plan and assumptions are recorded in:

```text
.ai/plan.md
```

One early design idea was to configure a single threshold for each device type. After reviewing the sample data, I noticed that two temperature sensors could require different normal ranges. I therefore changed the design to store thresholds per device.

AI-generated suggestions were manually reviewed and verified using:

- Unit tests
- API integration tests
- FastAPI Swagger testing
- Manual dashboard testing

## Author

**Basa Narsimha**

GitHub: [Narsimhabasa](https://github.com/Narsimhabasa)