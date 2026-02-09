# jyotishganit-mcp

MCP (Model Context Protocol) server that exposes [jyotishganit](https://pypi.org/project/jyotishganit/) Vedic astrology calculations as tools for Cursor and other MCP clients. All tools share an LRU cache so repeated calls with the same birth details are instant.

## Installation

```bash
pip install jyotishganit-mcp
```

## Tools

| Tool | Description |
|------|-------------|
| **calculate_birth_chart** | Compute a full Vedic birth chart and return it as JSON-LD. |
| **get_panchanga** | Return Panchanga (tithi, nakshatra, yoga, karana, vaara) for the birth moment. |
| **get_planetary_positions** | Return D1 planetary positions: body, sign, degrees, nakshatra, house, dignity. |
| **get_dashas** | Return Vimshottari dasha periods: current and upcoming mahadashas. |
| **get_divisional_chart** | Return a divisional chart (e.g. d9 Navamsa, d10 Dasamsa). chart_code: d2-d60. |

All tools take birth details: birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, latitude, longitude, timezone_offset, and optional name, location_name. get_divisional_chart also requires chart_code (e.g. d9).

## Usage with Cursor

Add the server to your MCP config (e.g. ~/.cursor/mcp.json):

```json
{
  "mcpServers": {
    "jyotishganit": {
      "command": "jyotishganit-mcp"
    }
  }
}
```

Or with python -m:

```json
{
  "mcpServers": {
    "jyotishganit": {
      "command": "python",
      "args": ["-m", "jyotishganit_mcp"]
    }
  }
}
```

## CLI

Run the server over stdio (for use by MCP clients):

```bash
jyotishganit-mcp
```

Or:

```bash
python -m jyotishganit_mcp
```

## Example

Example tool call (birth: July 4, 1996, 9:10 AM, Karmala, India; IST +5:30):

- get_panchanga with the above birth details returns e.g. tithi: Krishna Chaturthi, nakshatra: Dhanishta, vaara: Thursday.
- calculate_birth_chart returns the full JSON-LD birth chart (person, ayanamsa, panchanga, D1 chart, divisional charts, ashtakavarga, dashas).

## Development

```bash
git clone <repo-url>
cd jyotishganit-mcp
pip install -e ".[dev]"
```

- **Lint and format:** ruff check src tests && ruff format src tests
- **Type check:** mypy src/
- **Tests:** pytest (first run may download ephemeris data)

## Offline / local Hipparcos data

Birth chart and panchanga calculations need the Hipparcos star catalog (`hip_main.dat`). By default, jyotishganit (via Skyfield) tries to download it from CDS. If you already have `hip_main.dat` on disk (e.g. in this repo) and want to avoid the download or run without network access, set:

```bash
export JYOTISHGANIT_HIP_MAIN_DAT=/path/to/hip_main.dat
```

Then start the MCP server (or run your script) with this env var set. For Cursor, you can set it in the MCP server config using `env`:

```json
{
  "mcpServers": {
    "jyotishganit": {
      "command": "jyotishganit-mcp",
      "env": {
        "JYOTISHGANIT_HIP_MAIN_DAT": "/absolute/path/to/hip_main.dat"
      }
    }
  }
}
```

See the [jyotishganit](https://pypi.org/project/jyotishganit/) documentation for the underlying calculation library.
