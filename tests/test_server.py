"""Placeholder tests for the MCP server package."""

from jyotishganit_mcp import __version__


def test_version_is_string() -> None:
    """Package exposes a non-empty version string."""
    assert isinstance(__version__, str)
    assert len(__version__) > 0
