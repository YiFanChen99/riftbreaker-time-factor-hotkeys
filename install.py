"""Install the Time Factor Hotkeys mod into The Riftbreaker's mods folder.

The game loads local mods from <game dir>/mods/, and the same folders are the
workspaces of the official Workspace Editor (The Riftbreaker - Tools), which
publishes them to Steam Workshop. A local mod must be a folder holding
<folder name>.manifest: the game reads the manifest only from a folder, and
lists a zip mod in its "incompatible mods" popup as game version "Unknown".

Publishing writes the Workshop item ID into the workspace's manifest
(steam_published_file). The next publish updates that item only while the ID
is there, so `install` never overwrites an existing manifest, and
`save-manifest` copies it back into this repository after a publish.

Usage:
    python install.py                  install, or reinstall after editing the files
    python install.py save-manifest    copy the workspace's manifest back here
    python install.py remove           delete the mod folder
    python install.py --game-dir DIR
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

DEFAULT_GAME_DIR = Path(r"D:\SteamLibrary\steamapps\common\Riftbreaker")
MOD_NAME = "time_factor_hotkeys"
SOURCE_DIR = Path(__file__).resolve().parent
MANIFEST = f"{MOD_NAME}.manifest"
# Copied on every install: the Lua code, the Workshop preview image
# (<workspace>.png, PNG 16:9, at least 512x288, at most 2 MB) and the change note.
REFRESHED_FILES = [f"{MOD_NAME}.png", "changelog.txt"]


def published_id(manifest: Path) -> str:
    match = re.search(r'steam_published_file "(\d+)"', manifest.read_text(encoding="utf-8"))
    return match.group(1) if match else "0"


def install(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    if (target / "lua").exists():
        shutil.rmtree(target / "lua")
    shutil.copytree(SOURCE_DIR / "lua", target / "lua")
    for name in REFRESHED_FILES:
        shutil.copy2(SOURCE_DIR / name, target / name)
    if (target / MANIFEST).exists():
        print(f"Kept the existing {MANIFEST} (Workshop item ID {published_id(target / MANIFEST)})")
    else:
        shutil.copy2(SOURCE_DIR / MANIFEST, target / MANIFEST)
    print(f"Installed {target}")
    for path in sorted(target.rglob("*")):
        if path.is_file():
            print(f"  {path.relative_to(target).as_posix()}")


def save_manifest(target: Path) -> None:
    source = target / MANIFEST
    if not source.exists():
        sys.exit(f"No manifest at {source}")
    shutil.copy2(source, SOURCE_DIR / MANIFEST)
    print(f"Copied {source} here (Workshop item ID {published_id(source)}); commit it")


def remove(target: Path) -> None:
    if not target.exists():
        print(f"Not installed: {target} does not exist")
        return
    if (target / MANIFEST).exists() and published_id(target / MANIFEST) != published_id(SOURCE_DIR / MANIFEST):
        sys.exit("The workspace's manifest holds a Workshop item ID this repository lacks; "
                 "run `python install.py save-manifest` first")
    shutil.rmtree(target)
    print(f"Removed {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install Time Factor Hotkeys into the mods folder.")
    parser.add_argument("action", nargs="?", choices=["install", "save-manifest", "remove"], default="install")
    parser.add_argument("--game-dir", type=Path, default=DEFAULT_GAME_DIR)
    arguments = parser.parse_args()
    if not (arguments.game_dir / "bin").is_dir():
        sys.exit(f"Not The Riftbreaker's install folder: {arguments.game_dir}")
    target = arguments.game_dir / "mods" / MOD_NAME
    {"install": install, "save-manifest": save_manifest, "remove": remove}[arguments.action](target)


if __name__ == "__main__":
    main()
