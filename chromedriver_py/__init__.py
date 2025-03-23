from __future__ import annotations

import subprocess
import sys
from importlib.resources import files
from os import PathLike
from pathlib import Path
from typing import Iterable


def binary_path() -> str:
    """deprecated, use `chromedriver_path` instead"""
    return str(chromedriver_path())


def chromedriver_path() -> Path:
    is_windows = sys.platform.startswith("win")
    binary_name = "chromedriver.exe" if is_windows else "chromedriver"
    binary_path = files("chromedriver_py").joinpath(binary_name)

    result = Path(str(binary_path))
    if not result.exists():
        raise FileNotFoundError(f"Could not find chromedriver binary at {result}")

    return result


def run_chromedriver(args: Iterable[str | PathLike]) -> int:
    return subprocess.run([chromedriver_path(), *args], check=False).returncode


def main(args: Iterable[str | PathLike] | None = None):
    if args is None:
        args = sys.argv[1:]
    return run_chromedriver(args)


if __name__ == "__main__":
    sys.exit(main())
