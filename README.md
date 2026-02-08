# jyotishganit-mcp

MCP (Model Context Protocol) server that exposes [jyotishganit](https://pypi.org/project/jyotishganit/) Vedic astrology calculations as tools and resources for Cursor and other MCP clients.

## Installation

```bash
pip install jyotishganit-mcp
```

## Development

```bash
git clone <repo-url>
cd jyotishganit-mcp
pip install -e ".[dev]"
```

- **Lint and format:** `ruff check src tests && ruff format src tests`
- **Type check:** `mypy src/`
- **Tests:** `pytest`

See the [jyotishganit](https://pypi.org/project/jyotishganit/) documentation for the underlying calculation library.
