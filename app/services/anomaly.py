from dataclasses import dataclass


@dataclass(frozen=True)
class AnomalyResult:
    """Result produced after checking one reading."""

    is_anomaly: bool
    message: str | None


def evaluate_reading(
    *,
    value: float,
    normal_min: float,
    normal_max: float,
    unit: str,
) -> AnomalyResult:
    """Check whether a reading is outside its configured normal range."""

    if normal_min >= normal_max:
        raise ValueError("normal_min must be less than normal_max")

    if value < normal_min:
        return AnomalyResult(
            is_anomaly=True,
            message=(
                f"Reading {value:g} {unit} is below the normal range "
                f"of {normal_min:g} to {normal_max:g} {unit}."
            ),
        )

    if value > normal_max:
        return AnomalyResult(
            is_anomaly=True,
            message=(
                f"Reading {value:g} {unit} is above the normal range "
                f"of {normal_min:g} to {normal_max:g} {unit}."
            ),
        )

    return AnomalyResult(is_anomaly=False, message=None)