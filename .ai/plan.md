# Device Monitoring Service — Implementation Plan

## Goal

Build a small full-stack service for managing devices, recording readings,
detecting abnormal values, and resolving alerts.

## Technology Choices

- FastAPI for the REST API
- SQLAlchemy for database access
- SQLite for local persistence
- Pydantic for request and response validation
- HTML, CSS, and JavaScript for the frontend
- Pytest for automated tests

## Core Features

- [ ] Create, list, update, and delete devices
- [ ] Submit readings for active devices
- [ ] Filter readings by start and end time
- [ ] Detect readings outside a device's normal range
- [ ] Create alerts automatically
- [ ] List unresolved alerts
- [ ] Resolve an alert
- [ ] Display devices, readings, and alerts in a single-page UI
- [ ] Test important business rules
- [ ] Document setup instructions and design decisions

## Design Assumptions

- Normal ranges are stored per device because the sample data shows two
  temperature sensors with different safe ranges.
- Active devices must have a unit, minimum threshold, and maximum threshold.
- Inactive devices cannot accept new readings.
- A value is normal when `minimum <= value <= maximum`.
- Every out-of-range reading creates one alert.
- Timestamps are stored in UTC.
- Alert records retain the reading that caused them.
- Sustained-anomaly detection is outside the initial scope but could be added
  using consecutive readings or a time window.

## Planned Development Order

1. Create the project structure and dependencies.
2. Implement database models and schemas.
3. Implement device CRUD.
4. Implement readings and anomaly detection.
5. Implement alerts and resolution.
6. Build the frontend.
7. Add automated tests.
8. Complete the README and final review.

## AI-Assisted Workflow

AI will be used for planning, generating small code sections, reviewing errors,
and suggesting tests. Each part will be reviewed and tested before moving to
the next feature. Incorrect suggestions and corrections will be recorded in a
separate AI notes file.