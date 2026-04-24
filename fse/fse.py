# fse/fse.py
# Entry point

import sys
from pathlib import Path

script_dir = Path(__file__).absolute()
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from fse.cmd import COMMANDS
from fse.cli.general.aliases import resolve
from fse.cli.general.errors import unknown_command, handle_interrupt, handle_exception

from fse.cli.commands.general import about as cmd_about
from fse.cli.commands.general import version as cmd_version
from fse.cli.commands.general import help as cmd_help
from fse.cli.commands.general import status as cmd_status


SPECIAL = {
    "--help":     cmd_help.run,
    "--about":    cmd_about.run,
    "--version":  cmd_version.run,
    "version":    cmd_version.run,
    "--aliases":  cmd_help.run_aliases,
    "--status":   cmd_status.run,
}


def main():
    if len(sys.argv) < 2:
        cmd_about.run()
        return

    args = resolve(sys.argv[1:])
    cmd = args[0].lower()
    cmd_args = args[1:]

    if cmd in SPECIAL:
        SPECIAL[cmd]()
        return

    if cmd not in COMMANDS:
        unknown_command(cmd)

    _, handler = COMMANDS[cmd]

    try:
        handler(cmd_args)
    except KeyboardInterrupt:
        handle_interrupt()
        sys.exit(130)
    except Exception as e:
        handle_exception(e)


if __name__ == "__main__":
    main()