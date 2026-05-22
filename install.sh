#!/usr/bin/env bash
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_KEY="mayank-skills@local"
CLAUDE_DIR="$HOME/.claude"
PLUGINS_FILE="$CLAUDE_DIR/plugins/installed_plugins.json"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

# Verify Claude Code is installed
if [[ ! -d "$CLAUDE_DIR" ]]; then
  echo "Error: ~/.claude not found. Install Claude Code first." >&2
  exit 1
fi

PLUGIN_VERSION="$(python3 -c "import json; print(json.load(open('$PLUGIN_DIR/.claude-plugin/plugin.json'))['version'])")"

echo "Installing mayank-skills v$PLUGIN_VERSION from $PLUGIN_DIR ..."

# Register in installed_plugins.json
python3 << EOF
import json, os, datetime

plugins_file = "$PLUGINS_FILE"
os.makedirs(os.path.dirname(plugins_file), exist_ok=True)

if os.path.exists(plugins_file):
    with open(plugins_file) as f:
        data = json.load(f)
else:
    data = {"version": 2, "plugins": {}}

data["plugins"]["$PLUGIN_KEY"] = [{
    "scope": "user",
    "installPath": "$PLUGIN_DIR",
    "version": "$PLUGIN_VERSION",
    "installedAt": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
}]

with open(plugins_file, "w") as f:
    json.dump(data, f, indent=2)

print("  registered in installed_plugins.json")
EOF

# Enable in settings.json
python3 << EOF
import json, os

settings_file = "$SETTINGS_FILE"

if not os.path.exists(settings_file):
    print("  ~/.claude/settings.json not found — skipping (enable manually)")
else:
    with open(settings_file) as f:
        data = json.load(f)

    data.setdefault("enabledPlugins", {})["$PLUGIN_KEY"] = True

    with open(settings_file, "w") as f:
        json.dump(data, f, indent=2)

    print("  enabled in settings.json")
EOF

echo ""
echo "Done. Restart Claude Code to activate the plugin."
