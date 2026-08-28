# AI Development Notes

## Corrections Made During Implementation

- Replaced timezone-naive default timestamps with UTC-aware timestamps.
- Added a SQLAlchemy UTC datetime type so SQLite timestamps are restored with UTC timezone information.
- Normalized timezone-aware reading-filter parameters to UTC and rejected filters that do not include timezone information.
- Added tests for timezone validation and filtering behaviour.
- Corrected frontend timestamp parsing so timestamps without explicit offsets are treated as UTC.
- Removed duplicate imports and helper functions and corrected code formatting.

## Design Decisions

- Thresholds are configured per device because acceptable ranges depend on the device and measurement type.
- Minimum and maximum threshold values are considered normal; alerts are created only for values outside that inclusive range.
- Alerts are resolved instead of deleted so the monitoring history is preserved.
- SQLite provides a simple local setup, while SQLAlchemy keeps the persistence layer replaceable.