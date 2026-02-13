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

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hip_main_dat = os.path.join(repo_root, "hip_main.dat")

    data["mcpServers"]["jyotishganit"] = {
        "type": "stdio",
        "command": sys.executable,
        "args": ["-m", "jyotishganit_mcp"],
        "env": {"JYOTISHGANIT_HIP_MAIN_DAT": hip_main_dat},
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("Registered jyotishganit MCP in", path)
    print("  env JYOTISHGANIT_HIP_MAIN_DAT =", hip_main_dat)


if __name__ == "__main__":
    main()
