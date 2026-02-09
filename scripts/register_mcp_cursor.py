"""Register jyotishganit MCP server in Cursor's ~/.cursor/mcp.json."""

import json
import os
import sys


def main() -> None:
    path = os.path.expanduser("~/.cursor/mcp.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    if "mcpServers" not in data:
        data["mcpServers"] = {}
    data["mcpServers"]["jyotishganit"] = {
        "command": sys.executable,
        "args": ["-m", "jyotishganit_mcp"],
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("Registered jyotishganit MCP in", path)


if __name__ == "__main__":
    main()
