"""LRU-cached birth chart computation for jyotishganit."""

from __future__ import annotations

import dataclasses
import functools
from datetime import datetime
from typing import TYPE_CHECKING

from jyotishganit import calculate_birth_chart
from jyotishganit.core.models import Person

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
    """Return a Vedic birth chart, using LRU cache for same birth details.

    The cache key is (birth_date, lat, lon, timezone_offset) only; name and
    location_name do not affect calculations. If the caller provides name,
    the returned chart's person is patched so the full JSON-LD has the
    correct label. (location_name is not stored by jyotishganit's Person.)
    """
    chart = _get_birth_chart_cached(
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
    if name is not None and name != "":
        p = chart.person
        new_person = Person(
            birth_datetime=p.birth_datetime,
            latitude=p.latitude,
            longitude=p.longitude,
            timezone_offset=p.timezone_offset,
            timezone=p.timezone,
            name=name,
        )
        chart = dataclasses.replace(chart, person=new_person)
    return chart


def clear_cache() -> None:
    """Clear the birth chart cache. Used for testing."""
    _get_birth_chart_cached.cache_clear()
