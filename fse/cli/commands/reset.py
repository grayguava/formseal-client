# fse/cli/commands/reset.py
# Reset command - remove and re-scaffold

import shutil

from fse.cli.ui import br, ok
from fse.cli.general.helpers import SRC, DEST


def run(_=None):
    if DEST.exists():
        shutil.rmtree(DEST)

    shutil.copytree(SRC, DEST)

    br()
    ok("re-initialized")
    br()