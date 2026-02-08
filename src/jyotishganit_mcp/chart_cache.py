"""LRU-cached birth chart computation for jyotishganit."""

from __future__ import annotations

import functools
from datetime import datetime
from typing import TYPE_CHECKING

from jyotishganit import calculate_birth_chart

if TYPE_CHECKING:
    from jyotishganit.core.models import VedicBirthChart

_CACHE_MAXSIZE = 32


@functools.lru_cache(maxsize=_CACHE_MAXSIZE)
def _get_birth_chart_cached(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
) -> VedicBirthChart:
    """Compute birth chart; result is cached by birth details."""
    birth_date = datetime(year, month, day, hour, minute, second)
    return calculate_birth_chart(
        birth_date=birth_date,
        latitude=latitude,
        longitude=longitude,
        timezone_offset=timezone_offset,
        location_name=None,
        name=None,
    )


def get_birth_chart(
    birth_date: datetime,
    latitude: float,
    longitude: float,
    timezone_offset: float = 0.0,
    location_name: str | None = None,
    name: str | None = None,
) -> VedicBirthChart:
    """Return a Vedic birth chart, using LRU cache for same birth details."""
    return _get_birth_chart_cached(
        birth_date.year,
        birth_date.month,
        birth_date.day,
        birth_date.hour,
        birth_date.minute,
        birth_date.second,
        latitude,
        longitude,
        timezone_offset,
    )


def clear_cache() -> None:
    """Clear the birth chart cache. Used for testing."""
    _get_birth_chart_cached.cache_clear()
