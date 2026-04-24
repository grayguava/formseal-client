# fse/general/errors.py
# Error handlers

from fse.cli.ui import fail, br


def unknown_command(cmd):
    br()
    fail(f"Unknown command: {cmd}\n{' '*19}Run 'fse --help' for available commands")


def command_not_implemented(cmd):
    br()
    fail(f"Command not implemented: {cmd}")


def handle_interrupt():
    from fse.cli.ui import info
    br()
    info("Interrupted.")
    br()


def handle_exception(e):
    from fse.cli.ui import fail
    fail(str(e))