from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Device
from app.schemas import (
    DeviceCreate,
    DeviceResponse,
    DeviceStatus,
    DeviceType,
    DeviceUpdate,
    MessageResponse,
)


router = APIRouter(prefix="/api/devices", tags=["devices"])


def get_device_or_404(device_id: str, database: Session) -> Device:
    """Return a device or raise a 404 error."""

    device = database.get(Device, device_id)

    if device is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    return device


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=http_status.HTTP_201_CREATED,
)
def create_device(
    device_data: DeviceCreate,
    database: Session = Depends(get_db),
) -> Device:
    """Create a new device."""

    device = Device(**device_data.model_dump())

    database.add(device)
    database.commit()
    database.refresh(device)

    return device


@router.get("", response_model=list[DeviceResponse])
def list_devices(
    device_status: DeviceStatus | None = Query(
        default=None,
        alias="status",
    ),
    device_type: DeviceType | None = Query(
        default=None,
        alias="type",
    ),
    database: Session = Depends(get_db),
) -> list[Device]:
    """List devices, optionally filtered by status or type."""

    query = select(Device).order_by(Device.name)

    if device_status is not None:
        query = query.where(Device.status == device_status)

    if device_type is not None:
        query = query.where(Device.type == device_type)

    return list(database.scalars(query).all())


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: str,
    database: Session = Depends(get_db),
) -> Device:
    """Fetch one device by its ID."""

    return get_device_or_404(device_id, database)


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: str,
    device_data: DeviceUpdate,
    database: Session = Depends(get_db),
) -> Device:
    """Replace the editable information for an existing device."""

    device = get_device_or_404(device_id, database)

    for field_name, value in device_data.model_dump().items():
        setattr(device, field_name, value)

    database.commit()
    database.refresh(device)

    return device


@router.delete(
    "/{device_id}",
    response_model=MessageResponse,
)
def delete_device(
    device_id: str,
    database: Session = Depends(get_db),
) -> MessageResponse:
    """Delete a device and its associated readings and alerts."""

    device = get_device_or_404(device_id, database)

    database.delete(device)
    database.commit()

    return MessageResponse(message="Device deleted successfully")