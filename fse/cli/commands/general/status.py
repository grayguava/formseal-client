# fse/cli/commands/general/status.py
# Status command - show current config

import json
import re

from fse.cli.ui import br, header, warn, D, W, R, GRAY
from fse.cli.general.helpers import DEST


def run():
    br()
    header("status")
    br()

    print(f"  {D}Configuration Status:{R}")
    br()

    config_path = DEST / "config" / "fse.config.js"

    if not config_path.exists():
        warn("formseal-embed not initialized. Run fse init first.")
        br()
        return

    content = config_path.read_text(encoding="utf-8")

    def row(label, value, color=W):
        print(f"  {D}{label:<20}{R}{color}{value}{R}")

    ep_match = re.search(r'endpoint:\s*"([^"]+)"', content)
    row("POST API:", ep_match.group(1) if ep_match else "(not set)", W if ep_match else GRAY)

    key_match = re.search(r'publicKey:\s*"([A-Za-z0-9_-]+)"', content)
    row("Public Key:", key_match.group(1) if key_match else "(not set)", W if key_match else GRAY)

    origin_match = re.search(r'origin:\s*"([^"]+)"', content)
    row("Origin:", origin_match.group(1) if origin_match else "(not set)", W if origin_match else GRAY)

    fields_path = DEST / "config" / "fields.jsonl"
    if fields_path.exists():
        content = fields_path.read_text(encoding="utf-8").strip()
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        count = sum(1 for l in lines if json.loads(l))
        row("Total Fields:", str(count))
    else:
        row("Total Fields:", "0", GRAY)

    br()