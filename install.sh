#!/usr/bin/env bash
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
MARKETPLACE="mayank-skills"
PLUGIN_KEY="mayank-skills@mayank-skills"
GITHUB_REPO="mayankdharwa/agent-skills"
CLAUDE_DIR="$HOME/.claude"
PLUGINS_FILE="$CLAUDE_DIR/plugins/installed_plugins.json"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
KNOWN_MARKETPLACES_FILE="$CLAUDE_DIR/plugins/known_marketplaces.json"

# Verify Claude Code is installed
if [[ ! -d "$CLAUDE_DIR" ]]; then
  echo "Error: ~/.claude not found. Install Claude Code first." >&2
  exit 1
fi

PLUGIN_VERSION="$(python3 -c "import json; print(json.load(open('$PLUGIN_DIR/.claude-plugin/plugin.json'))['version'])")"

echo "Installing mayank-skills v$PLUGIN_VERSION from $PLUGIN_DIR ..."

# 1. Register marketplace in known_marketplaces.json
python3 << EOF
import json, os

f = "$KNOWN_MARKETPLACES_FILE"
if os.path.exists(f):
    with open(f) as fh:
        data = json.load(fh)
else:
    data = {}

data["$MARKETPLACE"] = {
    "source": {"source": "github", "repo": "$GITHUB_REPO"},
    "installLocation": "$CLAUDE_DIR/plugins/marketplaces/$MARKETPLACE"
}

with open(f, "w") as fh:
    json.dump(data, fh, indent=2)

print("  registered marketplace in known_marketplaces.json")
EOF

# 2. Register plugin in installed_plugins.json
python3 << EOF
import json, os, datetime

f = "$PLUGINS_FILE"
os.makedirs(os.path.dirname(f), exist_ok=True)
data = json.load(open(f)) if os.path.exists(f) else {"version": 2, "plugins": {}}

data["plugins"]["$PLUGIN_KEY"] = [{
    "scope": "user",
    "installPath": "$PLUGIN_DIR",
    "version": "$PLUGIN_VERSION",
    "installedAt": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
}]

with open(f, "w") as fh:
    json.dump(data, fh, indent=2)

print("  registered in installed_plugins.json")
EOF

# 3. Enable in settings.json
python3 << EOF
import json, os

f = "$SETTINGS_FILE"
if not os.path.exists(f):
    print("  ~/.claude/settings.json not found — skipping (enable manually)")
else:
    with open(f) as fh:
        data = json.load(fh)

    data.setdefault("enabledPlugins", {})["$PLUGIN_KEY"] = True
    data.setdefault("extraKnownMarketplaces", {})["$MARKETPLACE"] = {
        "source": {"source": "github", "repo": "$GITHUB_REPO"}
    }

    # Clean up old @local entry if present
    data["enabledPlugins"].pop("mayank-skills@local", None)

    with open(f, "w") as fh:
        json.dump(data, fh, indent=2)

    print("  enabled in settings.json")
EOF

echo ""
echo "Done. Run /reload-plugins in Claude Code to activate."
