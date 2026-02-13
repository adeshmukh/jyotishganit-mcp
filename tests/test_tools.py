"""Tests for MCP server tools using known birth data (July 4, 1996, Karmala)."""

import json

from jyotishganit_mcp.chart_cache import clear_cache
from jyotishganit_mcp.server import (
    calculate_birth_chart,
    get_dashas,
    get_divisional_chart,
    get_panchanga,
    get_planetary_positions,
)

# Known birth data from jyotishganit docs: Karmala, India
BIRTH = {
    "birth_year": 1996,
    "birth_month": 7,
    "birth_day": 4,
    "birth_hour": 9,
    "birth_minute": 10,
    "birth_second": 0,
    "latitude": 18.404,
    "longitude": 75.195,
    "timezone_offset": 5.5,
    "name": "",
    "location_name": "",
}


def test_calculate_birth_chart_returns_valid_json() -> None:
    """calculate_birth_chart returns valid JSON with expected top-level keys."""
    clear_cache()
    result = calculate_birth_chart(**BIRTH)
    data = json.loads(result)
    assert "@context" in data
    assert "@type" in data
    assert data["@type"] == "VedicBirthChart"
    assert "person" in data
    assert "d1_chart" in data or "d1Chart" in data or "d1_chart" in str(data).lower()


def test_calculate_birth_chart_passes_through_name() -> None:
    """calculate_birth_chart includes caller-provided name in person metadata."""
    clear_cache()
    result = calculate_birth_chart(**{**BIRTH, "name": "Bhampu"})
    data = json.loads(result)
    assert data["person"]["name"] == "Bhampu"


def test_get_panchanga_returns_expected_fields() -> None:
    """get_panchanga returns tithi, nakshatra, yoga, karana, vaara."""
    clear_cache()
    result = get_panchanga(**BIRTH)
    assert "tithi" in result
    assert "nakshatra" in result
    assert "yoga" in result
    assert "karana" in result
    assert "vaara" in result
    assert result["nakshatra"] == "Dhanishta"
    assert result["tithi"] == "Krishna Chaturthi"


def test_get_planetary_positions_returns_nine_planets() -> None:
    """get_planetary_positions returns 9 planets with expected fields."""
    clear_cache()
    result = get_planetary_positions(**BIRTH)
    assert len(result) == 9
    for p in result:
        assert "celestial_body" in p
        assert "sign" in p
        assert "sign_degrees" in p
        assert "nakshatra" in p
        assert "house" in p
        assert "motion_type" in p
        assert "dignity" in p
    bodies = [p["celestial_body"] for p in result]
    assert "Moon" in bodies
    assert "Sun" in bodies


def test_get_dashas_returns_current_and_upcoming() -> None:
    """get_dashas returns current and upcoming mahadashas."""
    clear_cache()
    result = get_dashas(**BIRTH)
    assert "current" in result
    assert "upcoming" in result
    assert "mahadashas" in result["current"]
    assert "mahadashas" in result["upcoming"]


def test_get_divisional_chart_d9_returns_houses_and_planets() -> None:
    """get_divisional_chart for d9 returns Navamsa with houses and ascendant."""
    clear_cache()
    result = get_divisional_chart(**BIRTH, chart_code="d9")
    assert isinstance(result, dict)
    assert "ascendant" in result or "houses" in result
    if "houses" in result:
        assert len(result["houses"]) == 12
    # GitHub jyotishganit@main includes degrees in divisional charts
    if "ascendant" in result and "signDegrees" in result["ascendant"]:
        assert isinstance(result["ascendant"]["signDegrees"], (int, float))
    occupants_with_degrees = []
    for house in result.get("houses", []):
        for occ in house.get("occupants", []):
            if "signDegrees" in occ:
                occupants_with_degrees.append(occ)
    if occupants_with_degrees:
        assert isinstance(occupants_with_degrees[0]["signDegrees"], (int, float))


def test_get_divisional_chart_invalid_code_returns_error() -> None:
    """get_divisional_chart with invalid chart_code returns error message."""
    clear_cache()
    result = get_divisional_chart(**BIRTH, chart_code="d99")
    assert isinstance(result, str)
    assert "Unknown" in result or "Valid codes" in result
