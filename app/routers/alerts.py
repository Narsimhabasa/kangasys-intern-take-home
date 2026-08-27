from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert
from app.schemas import AlertResponse


router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    resolved: bool = Query(
        default=False,
        description="Choose false for active alerts or true for resolved alerts",
    ),
    device_id: str | None = Query(default=None),
    database: Session = Depends(get_db),
) -> list[Alert]:
    """List active or resolved alerts."""

    query = select(Alert).where(Alert.resolved == resolved)

    if device_id is not None:
        query = query.where(Alert.device_id == device_id)

    query = query.order_by(Alert.timestamp.desc())

    return list(database.scalars(query).all())


@router.patch(
    "/{alert_id}/resolve",
    response_model=AlertResponse,
)
def resolve_alert(
    alert_id: int,
    database: Session = Depends(get_db),
) -> Alert:
    """Mark an alert as resolved."""

    alert = database.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    if not alert.resolved:
        alert.resolved = True
        alert.resolved_at = datetime.now(timezone.utc)
        database.commit()
        database.refresh(alert)

    return alert