# fse/cli/ui/__init__.py
# UI module exports

from fse.cli.ui.styles import (
    RESET, BOLD, DIM,
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GRAY,
    O, S, G, C, Y, M, W, D, R,
    HEAD, OK, TICK, CROSS, XFATAL,
)
from fse.cli.ui.headers import header, rule
from fse.cli.ui.bodies import (
    br, badge, fail, row, cmd_line, code, link, ok, info, warn,
)