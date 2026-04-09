# commands/version.py
# Show version info and check for updates.

import json
import urllib.request
from pathlib import Path

from ui.output import br, rule, row, link, badge, C, G, Y, S, W, R, D, BOLD

PACKAGE_PATH = Path(__file__).resolve().parent.parent.parent / "package.json"
NPM_URL = "https://registry.npmjs.org/@formseal/embed/latest"


def run():
    local_version = _get_local_version()
    latest_version = _get_npm_version()

    br()
    print(f"{C} \u250c\u2500 {R}{W}formseal-embed{R}  {G}version{R}")
    print(G + " " + "\u2500" * 52 + R)
    br()

    row(">", "local", local_version)

    if latest_version:
        row(">", "npm", latest_version)
        br()

        if _compare_versions(local_version, latest_version) < 0:
            print(f"  {Y}Update available{R}")
            print(G + " " + "\u2500" * 52 + R)
            print(f"  {G}Run:{R}")
            print(f"    {W}npm install -g @formseal/embed{R}")
        else:
            print(f"  {G}Up to date{R}")
    else:
        print(f"  {S}Could not fetch npm version{R}")


def _get_local_version():
    try:
        content = PACKAGE_PATH.read_text(encoding="utf-8")
        data = json.loads(content)
        return data.get("version", "unknown")
    except:
        return "unknown"


def _get_npm_version():
    try:
        req = urllib.request.Request(NPM_URL)
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("version", None)
    except:
        return None


def _compare_versions(local, npm):
    local_parts = [int(x) for x in local.split(".")]
    npm_parts = [int(x) for x in npm.split(".")]

    for l, n in zip(local_parts, npm_parts):
        if l < n:
            return -1
        elif l > n:
            return 1
    return 0
