"""Install or remove the Time Factor Hotkeys mod for The Riftbreaker.

The game loads local mods from <game dir>/mods/. A local mod must be a folder
holding <folder name>.manifest (the WorkspaceManifest format Steam Workshop
mods use): the game reads the manifest only from a folder, and lists a zip
mod in its "incompatible mods" popup as game version "Unknown". This mod adds
one Lua file whose name ends in `_autoexec.lua`, which the game runs every
time a map is created.

Usage:
    python install.py            install, or reinstall after editing the Lua file
    python install.py remove     delete the mod folder
    python install.py --game-dir DIR
"""

import argparse
import base64
import shutil
import sys
from pathlib import Path

DEFAULT_GAME_DIR = Path(r"D:\SteamLibrary\steamapps\common\Riftbreaker")
MOD_NAME = "time_factor_hotkeys"
VERSION = "1.0.0"
# The version the mod was made against, in the game's own "EXE: x DATA: y" form.
GAME_VERSION = "EXE: 1186 DATA: 847"
TITLE = "Time Factor Hotkeys"
DESCRIPTION = "Binds F1-F4 to time_factor 0.3, 1, 1.5 and 3."
SOURCE_DIR = Path(__file__).resolve().parent


def encoded(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def manifest() -> str:
    return f"""WorkspaceManifest
{{
	description "{encoded(DESCRIPTION)}"
	tags
	{{
		String "Other"
	}}

	modified_game_files
	title "{encoded(TITLE)}"
	homepage
	modio_published_file "0"
	visibility "0"
	game_version "{GAME_VERSION}"
	version "{VERSION}"
	localizations
	author
	steam_published_file "0"
	dependencies
}}
"""


def install(game_dir: Path) -> None:
    target = game_dir / "mods" / MOD_NAME
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(SOURCE_DIR / "lua", target / "lua")
    (target / f"{MOD_NAME}.manifest").write_text(manifest(), encoding="utf-8")
    print(f"Installed {target}")
    for path in sorted(target.rglob("*")):
        if path.is_file():
            print(f"  {path.relative_to(target).as_posix()}")


def remove(game_dir: Path) -> None:
    target = game_dir / "mods" / MOD_NAME
    if target.exists():
        shutil.rmtree(target)
        print(f"Removed {target}")
    else:
        print(f"Not installed: {target} does not exist")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install or remove Time Factor Hotkeys.")
    parser.add_argument("action", nargs="?", choices=["install", "remove"], default="install")
    parser.add_argument("--game-dir", type=Path, default=DEFAULT_GAME_DIR)
    arguments = parser.parse_args()
    if not (arguments.game_dir / "bin").is_dir():
        sys.exit(f"Not The Riftbreaker's install folder: {arguments.game_dir}")
    {"install": install, "remove": remove}[arguments.action](arguments.game_dir)


if __name__ == "__main__":
    main()
