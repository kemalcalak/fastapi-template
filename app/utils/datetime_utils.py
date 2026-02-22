from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return the current datetime in UTC timezone."""
    return datetime.now(UTC)
