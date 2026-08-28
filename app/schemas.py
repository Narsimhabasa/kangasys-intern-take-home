from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Literal
def utc_now() -> datetime:
    return datetime.now(timezone.utc)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


DeviceType = Literal[
    "temperature-sensor",
    "pressure-gauge",
    "humidity-sensor",
    "energy-meter",
    "contact-sensor",
]

DeviceStatus = Literal["active", "inactive"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DeviceBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: DeviceType
    status: DeviceStatus = "active"
    unit: str = Field(min_length=1, max_length=20)
    normal_min: float | None = Field(default=None, allow_inf_nan=False)
    normal_max: float | None = Field(default=None, allow_inf_nan=False)

    @field_validator("name", "unit")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("value must not be blank")

        return cleaned_value

    @model_validator(mode="after")
    def validate_normal_range(self) -> DeviceBase:
        has_minimum = self.normal_min is not None
        has_maximum = self.normal_max is not None

        if has_minimum != has_maximum:
            raise ValueError(
                "normal_min and normal_max must be provided together"
            )

        if self.status == "active" and not has_minimum:
            raise ValueError(
                "active devices must have a normal minimum and maximum"
            )

        if (
            self.normal_min is not None
            and self.normal_max is not None
            and self.normal_min >= self.normal_max
        ):
            raise ValueError("normal_min must be less than normal_max")

        return self


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReadingCreate(BaseModel):
    value: float = Field(allow_inf_nan=False)
    unit: str = Field(min_length=1, max_length=20)
    timestamp: datetime = Field(default_factory=utc_now)

    @field_validator("unit")
    @classmethod
    def unit_must_not_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("unit must not be blank")

        return cleaned_value

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_include_timezone(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must include a timezone")

        return value.astimezone(timezone.utc)


class ReadingResponse(BaseModel):
    id: int
    device_id: str
    value: float
    unit: str
    timestamp: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertResponse(BaseModel):
    id: int
    device_id: str
    reading_id: int
    trigger_value: float
    unit: str
    timestamp: datetime
    message: str
    resolved: bool
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ReadingSubmissionResponse(BaseModel):
    reading: ReadingResponse
    alert: AlertResponse | None


class MessageResponse(BaseModel):
    message: str 