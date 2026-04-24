# fse/cli/commands/set.py
# Set command - configure endpoint and key

from fse.cli.ui import br, row, W, R, S, G, GRAY, CROSS, fail, rule
from fse.cli.general.helpers import _normalize_endpoint, _patch_config, _validate_key, CONFIG_PATH


def run(args):
    if not args:
        fail("Usage: fse set <endpoint|key> [value]")

    subcommand = args[0]
    cmd_args = args[1:]

    if not CONFIG_PATH.exists():
        fail(
            "formseal-embed/config/fse.config.js not found.\n"
            f"           Run fse init first."
        )

    if subcommand in ("endpoint", "ep"):
        _set_endpoint(cmd_args)
    elif subcommand in ("key", "k"):
        _set_key(cmd_args)
    else:
        fail(f"Unknown: {subcommand}\n" +
             f"           Use fse set endpoint or fse set key")


def _set_endpoint(args):
    value = args[0] if args else None

    if not value:
        value = _prompt_loop_endpoint()
        if not value:
            return

    original = value
    url = _normalize_endpoint(original)

    if not url.startswith("https://"):
        print(f"{CROSS} Endpoint must use HTTPS")
        return

    if not original.startswith("http://") and not original.startswith("https://"):
        br()
        print(f"  {GRAY}ℹ No protocol provided — using https://{R}")

    _patch_config("endpoint", url)
    br()
    print(f"  {S}*{R} {G}Updated!{R}")
    rule()
    row(">", "endpoint", url)


def _prompt_loop_endpoint():
    while True:
        value = _prompt("POST endpoint")
        if not value:
            print(f"  {GRAY}skipped{R}")
            return None

        url = _normalize_endpoint(value)
        if url.startswith("https://"):
            if value != url:
                print(f"  {GRAY}ℹ No protocol provided — using https://{R}")
            return url

        print(f"{CROSS} Endpoint must use HTTPS")


def _set_key(args):
    value = args[0] if args else None

    if not value:
        value = _prompt_loop_key()
        if not value:
            return

    if not _validate_key(value):
        br()
        print(f"{CROSS}  Invalid public key")
        print(f"  Expected raw 32-byte X25519 public key in base64url format")
        br()
        return

    _patch_config("key", value)
    br()
    print(f"  {S}*{R} {G}Updated!{R}")
    rule()
    row(">", "key", value[:24] + "...")


def _prompt_loop_key():
    while True:
        value = _prompt("X25519 public key")
        if not value:
            print(f"  {GRAY}skipped{R}")
            return None

        if _validate_key(value):
            return value

        print(f"{CROSS}  Invalid public key")
        print(f"  Expected raw 32-byte X25519 public key in base64url format")


from fse.cli.general.helpers import _prompt