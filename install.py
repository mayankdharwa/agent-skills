#!/usr/bin/env python3
import json
import os
import sys
import datetime
from pathlib import Path

MARKETPLACE = "mayank-skills"
PLUGIN_KEY = "mayank-skills@mayank-skills"
GITHUB_REPO = "mayankdharwa/agent-skills"

PLUGIN_DIR = Path(__file__).parent.resolve() / "plugin"
CLAUDE_DIR = Path.home() / ".claude"
PLUGINS_FILE = CLAUDE_DIR / "plugins" / "installed_plugins.json"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
KNOWN_MARKETPLACES_FILE = CLAUDE_DIR / "plugins" / "known_marketplaces.json"


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def main():
    if not CLAUDE_DIR.exists():
        sys.exit("Error: ~/.claude not found. Install Claude Code first.")

    plugin_manifest = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
    version = json.loads(plugin_manifest.read_text())["version"]

    print(f"Installing mayank-skills v{version} from {PLUGIN_DIR} ...")

    # 1. Register marketplace in known_marketplaces.json
    marketplaces = load_json(KNOWN_MARKETPLACES_FILE, {})
    marketplaces[MARKETPLACE] = {
        "source": {"source": "github", "repo": GITHUB_REPO},
        "installLocation": str(CLAUDE_DIR / "plugins" / "marketplaces" / MARKETPLACE),
        "lastUpdated": now_utc(),
    }
    save_json(KNOWN_MARKETPLACES_FILE, marketplaces)
    print("  registered marketplace in known_marketplaces.json")

    # 2. Register plugin in installed_plugins.json
    plugins = load_json(PLUGINS_FILE, {"version": 2, "plugins": {}})
    plugins["plugins"][PLUGIN_KEY] = [{
        "scope": "user",
        "installPath": str(PLUGIN_DIR),
        "version": version,
        "installedAt": now_utc(),
        "lastUpdated": now_utc(),
    }]
    save_json(PLUGINS_FILE, plugins)
    print("  registered in installed_plugins.json")

    # 3. Enable in settings.json
    if not SETTINGS_FILE.exists():
        print("  ~/.claude/settings.json not found — skipping (enable manually)")
    else:
        settings = load_json(SETTINGS_FILE, {})
        settings.setdefault("enabledPlugins", {})[PLUGIN_KEY] = True
        settings.setdefault("extraKnownMarketplaces", {})[MARKETPLACE] = {
            "source": {"source": "github", "repo": GITHUB_REPO}
        }
        settings["enabledPlugins"].pop("mayank-skills@local", None)
        save_json(SETTINGS_FILE, settings)
        print("  enabled in settings.json")

    print("\nDone. Run /reload-plugins in Claude Code to activate.")


if __name__ == "__main__":
    main()
