"""MCP server entry point and tool/resource definitions."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from jyotishganit import get_birth_chart_json_string
from mcp.server.fastmcp import FastMCP

from jyotishganit_mcp.chart_cache import get_birth_chart

if TYPE_CHECKING:
    from jyotishganit.core.models import VedicBirthChart

mcp = FastMCP("Jyotishganit", json_response=True)


def _birth_datetime(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
) -> datetime:
    """Build datetime from components; raises ValueError for invalid values."""
    return datetime(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
    )


def _get_chart(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
    name: str = "",
    location_name: str = "",
) -> VedicBirthChart:
    """Get cached birth chart from birth details."""
    birth_date = _birth_datetime(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
    )
    return get_birth_chart(
        birth_date=birth_date,
        latitude=latitude,
        longitude=longitude,
        timezone_offset=timezone_offset,
        location_name=location_name or None,
        name=name or None,
    )


@mcp.tool()
def calculate_birth_chart(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
    name: str = "",
    location_name: str = "",
) -> str:
    """Compute a full Vedic birth chart and return it as JSON-LD."""
    chart = _get_chart(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
        latitude,
        longitude,
        timezone_offset,
        name,
        location_name,
    )
    return get_birth_chart_json_string(chart)


@mcp.tool()
def get_panchanga(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
    name: str = "",
    location_name: str = "",
) -> dict[str, str]:
    """Return Panchanga (tithi, nakshatra, yoga, karana, vaara) for the birth moment."""
    chart = _get_chart(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
        latitude,
        longitude,
        timezone_offset,
        name,
        location_name,
    )
    p = chart.panchanga
    return {
        "tithi": p.tithi,
        "nakshatra": p.nakshatra,
        "yoga": p.yoga,
        "karana": p.karana,
        "vaara": p.vaara,
    }


@mcp.tool()
def get_planetary_positions(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
    name: str = "",
    location_name: str = "",
) -> list[dict[str, str | int | float]]:
    """Return D1 planetary positions: body, sign, degrees, nakshatra, house, dignity."""
    chart = _get_chart(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
        latitude,
        longitude,
        timezone_offset,
        name,
        location_name,
    )
    out = []
    for planet in chart.d1_chart.planets:
        out.append(
            {
                "celestial_body": planet.celestial_body,
                "sign": planet.sign,
                "sign_degrees": planet.sign_degrees,
                "nakshatra": planet.nakshatra,
                "pada": planet.pada,
                "house": planet.house,
                "motion_type": planet.motion_type,
                "dignity": planet.dignities.dignity,
            }
        )
    return out


@mcp.tool()
def get_dashas(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
    name: str = "",
    location_name: str = "",
) -> dict[str, object]:
    """Return Vimshottari dasha periods: current and upcoming mahadashas."""
    chart = _get_chart(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
        latitude,
        longitude,
        timezone_offset,
        name,
        location_name,
    )
    return chart.dashas.to_dict()


@mcp.tool()
def get_divisional_chart(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    timezone_offset: float,
    chart_code: str,
    name: str = "",
    location_name: str = "",
) -> dict[str, object] | str:
    """Return a divisional chart (d9 Navamsa, d10 Dasamsa, etc.). chart_code: d2-d60."""
    chart_code_lower = chart_code.strip().lower()
    valid_codes = (
        "d2",
        "d3",
        "d4",
        "d7",
        "d9",
        "d10",
        "d12",
        "d16",
        "d24",
        "d27",
        "d30",
        "d60",
    )
    if chart_code_lower not in valid_codes:
        valid = ", ".join(valid_codes)
        return f"Unknown chart code: {chart_code!r}. Valid codes: {valid}"
    chart = _get_chart(
        birth_year,
        birth_month,
        birth_day,
        birth_hour,
        birth_minute,
        birth_second,
        latitude,
        longitude,
        timezone_offset,
        name,
        location_name,
    )
    if chart_code_lower not in chart.divisional_charts:
        return f"Chart {chart_code_lower} not found."
    return chart.divisional_charts[chart_code_lower].to_dict()


def main() -> None:
    """Run the MCP server over stdio (for CLI entry point)."""
    mcp.run(transport="stdio")
