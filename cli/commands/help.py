# commands/help.py
# Help command - shows all available commands

from ui.output import br, rule, cmd_line, link, C, G, Y, M, W, D, R


def run():
    br()
    print(f"{C} \u250c\u2500 {R}{W}formseal-embed{R}  {G}@formseal/embed{R}")
    print(G + " " + "\u2500" * 52 + R)
    br()

    # Scaffold
    print(f"  {G}>>{R} {Y}Scaffold{R}")
    print(G + " " + "\u2500" * 52 + R)
    cmd_line("fse init", "scaffold ./formseal-embed/ into current directory")
    br()

    # Configure
    print(f"  {G}>>{R} {Y}Configure{R}")
    print(G + " " + "\u2500" * 52 + R)
    cmd_line("fse configure quick", "set endpoint and public key")
    br()

    # Fields
    print(f"  {G}>>{R} {Y}Fields{R}")
    print(G + " " + "\u2500" * 52 + R)
    cmd_line("fse -f add <name> type:email", "add field (type required)")
    cmd_line("fse -f rm <name>", "remove field")
    cmd_line("fse -f required <name> required:true", "set field required")
    cmd_line("fse -f maxLen <name> maxLen:100", "set field max length")
    cmd_line("fse -f type <name> type:email", "set field type")
    br()

    # Update
    print(f"  {G}>>{R} {Y}Update{R}")
    print(G + " " + "\u2500" * 52 + R)
    cmd_line("fse update endpoint <url>", "update POST endpoint")
    cmd_line("fse update key <base64url>", "update X25519 public key")
    cmd_line("fse --version", "check version and updates")
    br()

    # Coming soon
    print(f"  {G}>>{R} {M}Coming Soon{R}")
    print(G + " " + "\u2500" * 52 + R)
    cmd_line("fse doctor", "validate config and schema")
    br()

    # Docs
    print(f"  {G}>>{R} {Y}Docs{R}")
    print(G + " " + "\u2500" * 52 + R)
    link("https://github.com/grayguava/formseal-embed/docs")
    br()
