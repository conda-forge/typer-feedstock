"""Handle custom (custom) build chain for `typer(-(slim|cli))`"""
import os
import sys
from subprocess import call
from pathlib import Path
import shutil
import site

PKG_NAME = os.environ["PKG_NAME"]
PKG_SRC = Path(os.environ["SRC_DIR"]) / PKG_NAME
DIST = PKG_SRC / "dist"

def pym(*args):
    args = [*map(str, args)]
    print(">>>", *args, flush=True)
    env = {
        **os.environ,
        # see https://github.com/tiangolo/typer/blob/0.12.1/pdm_build.py
        "TIANGOLO_BUILD_PACKAGE": PKG_NAME,
    }

    rc = call([sys.executable, "-m", *args], cwd=str(PKG_SRC), env=env)
    if rc:
        sys.exit(rc)

def main():
    pym("build", "--no-isolation", "--wheel", ".")
    pym(
        "pip",
        "install",
        "-vvv",
        "--no-deps",
        "--disable-pip-version-check",
        "--find-links=dist",
        "--no-index",
        PKG_NAME
    )
    if PKG_NAME == "typer":
        sp_dir = Path(site.getsitepackages()[0]) / "typer"
        print(f"removing duplicated {sp_dir}")
        shutil.rmtree(sp_dir)

    return 0

if __name__ == "__main__":
    sys.exit(main())
