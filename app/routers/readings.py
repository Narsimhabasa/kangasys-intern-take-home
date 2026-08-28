from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, Reading
from app.routers.devices import get_device_or_404
from app.schemas import (
    AlertResponse,
    ReadingCreate,
    ReadingResponse,
    ReadingSubmissionResponse,
)
from app.services.anomaly import evaluate_reading


router = APIRouter(
    prefix="/api/devices/{device_id}/readings",
    tags=["readings"],
)


def normalize_filter_time(
    value: datetime | None,
    parameter_name: str,
) -> datetime | None:
    """Require a timezone and normalize a filter value to UTC."""

    if value is None:
        return None

    if value.tzinfo is None or value.utcoffset() is None:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"{parameter_name} must include a timezone",
        )

    return value.astimezone(timezone.utc)


@router.post(
    "",
    response_model=ReadingSubmissionResponse,
    status_code=http_status.HTTP_201_CREATED,
)
def submit_reading(
    device_id: str,
    reading_data: ReadingCreate,
    database: Session = Depends(get_db),
) -> ReadingSubmissionResponse:
    """Store a reading and create an alert when it is abnormal."""

    device = get_device_or_404(device_id, database)

    if device.status != "active":
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Inactive devices cannot accept readings",
        )

    if reading_data.unit != device.unit:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Reading unit must be '{device.unit}'",
        )

    if device.normal_min is None or device.normal_max is None:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Device does not have a configured normal range",
        )

    reading = Reading(
        device_id=device.id,
        value=reading_data.value,
        unit=reading_data.unit,
        timestamp=reading_data.timestamp,
    )

    database.add(reading)
    database.flush()

    anomaly_result = evaluate_reading(
        value=reading.value,
        normal_min=device.normal_min,
        normal_max=device.normal_max,
        unit=reading.unit,
    )

    alert: Alert | None = None

    if anomaly_result.is_anomaly:
        alert = Alert(
            device_id=device.id,
            reading_id=reading.id,
            trigger_value=reading.value,
            unit=reading.unit,
            timestamp=reading.timestamp,
            message=(
                anomaly_result.message
                or "Reading is outside the normal range."
            ),
        )
        database.add(alert)

    database.commit()
    database.refresh(reading)

    if alert is not None:
        database.refresh(alert)

    return ReadingSubmissionResponse(
        reading=ReadingResponse.model_validate(reading),
        alert=(
            AlertResponse.model_validate(alert)
            if alert is not None
            else None
        ),
    )


@router.get("", response_model=list[ReadingResponse])
def list_readings(
    device_id: str,
    start_time: datetime | None = Query(default=None),
    end_time: datetime | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    database: Session = Depends(get_db),
) -> list[Reading]:
    """List recent readings, optionally filtered by time range."""

    get_device_or_404(device_id, database)

    start_time = normalize_filter_time(start_time, "start_time")
    end_time = normalize_filter_time(end_time, "end_time")

    if (
        start_time is not None
        and end_time is not None
        and start_time > end_time
    ):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="start_time must be before end_time",
        )

    query = select(Reading).where(Reading.device_id == device_id)

    if start_time is not None:
        query = query.where(Reading.timestamp >= start_time)

    if end_time is not None:
        query = query.where(Reading.timestamp <= end_time)

    query = query.order_by(Reading.timestamp.desc()).limit(limit)

    return list(database.scalars(query).all())
