"""Tests for the LRU-cached birth chart computation."""

from datetime import datetime

from jyotishganit_mcp.chart_cache import clear_cache, get_birth_chart


def test_same_params_return_same_cached_object() -> None:
    """Two calls with same birth details return the same chart object (cache hit)."""
    clear_cache()
    birth = datetime(1996, 7, 4, 9, 10, 0)
    lat, lon, tz = 18.404, 75.195, 5.5
    chart1 = get_birth_chart(birth, lat, lon, tz)
    chart2 = get_birth_chart(birth, lat, lon, tz)
    assert chart1 is chart2


def test_different_params_return_different_charts() -> None:
    """Different birth details produce different chart objects (cache miss)."""
    clear_cache()
    birth1 = datetime(1996, 7, 4, 9, 10, 0)
    birth2 = datetime(1996, 7, 4, 10, 10, 0)
    lat, lon, tz = 18.404, 75.195, 5.5
    chart1 = get_birth_chart(birth1, lat, lon, tz)
    chart2 = get_birth_chart(birth2, lat, lon, tz)
    assert chart1 is not chart2


def test_clear_cache_resets() -> None:
    """clear_cache() invalidates the cache so next call recomputes."""
    clear_cache()
    birth = datetime(1996, 7, 4, 9, 10, 0)
    lat, lon, tz = 18.404, 75.195, 5.5
    chart1 = get_birth_chart(birth, lat, lon, tz)
    clear_cache()
    chart2 = get_birth_chart(birth, lat, lon, tz)
    assert chart1 is not chart2
