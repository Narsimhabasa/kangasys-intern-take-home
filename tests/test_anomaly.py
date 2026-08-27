import pytest

from app.services.anomaly import evaluate_reading


@pytest.mark.parametrize("value", [2.0, 4.5, 8.0])
def test_readings_inside_or_on_boundaries_are_normal(value: float) -> None:
    result = evaluate_reading(
        value=value,
        normal_min=2.0,
        normal_max=8.0,
        unit="C",
    )

    assert result.is_anomaly is False
    assert result.message is None


def test_reading_below_minimum_is_anomaly() -> None:
    result = evaluate_reading(
        value=0.6,
        normal_min=1.5,
        normal_max=6.0,
        unit="bar",
    )

    assert result.is_anomaly is True
    assert result.message is not None
    assert "below" in result.message


def test_reading_above_maximum_is_anomaly() -> None:
    result = evaluate_reading(
        value=11.6,
        normal_min=2.0,
        normal_max=8.0,
        unit="C",
    )

    assert result.is_anomaly is True
    assert result.message is not None
    assert "above" in result.message


def test_invalid_range_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="normal_min must be less than normal_max",
    ):
        evaluate_reading(
            value=5.0,
            normal_min=8.0,
            normal_max=2.0,
            unit="C",
        )