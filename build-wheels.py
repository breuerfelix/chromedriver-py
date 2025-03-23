from __future__ import annotations

import io
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Literal, TypeAlias, cast

import requests

URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
PLATFORMS = {
    "linux64": "linux_x86_64",
    "mac-arm64": "macosx_11_0_arm64",
    "mac-x64": "macosx_10_9_x86_64",
    "win32": "win32",
    "win64": "win_amd64",
}
VERSION_FILE = "CURRENT_VERSION.txt"

Channel: TypeAlias = Literal["Canary", "Dev", "Beta", "Stable"]

prerelease_specifiers: dict[Channel, str] = {
    "Stable": "",
    "Beta": "b",
    "Dev": "a",
    "Canary": ".dev",
}


def fetch_latest_version(channel: Channel) -> tuple[str, dict[object, object]]:
    result = requests.get(URL, timeout=60).json()["channels"][channel]
    return result["version"], result


def pypi_exists(version: str) -> bool:
    url = f"https://pypi.org/pypi/chromedriver-py/{version}/json"
    response = requests.get(url)
    return response.status_code == 200


def download_and_build(channel_str: str):
    channel = cast("Channel", channel_str)
    version, result = fetch_latest_version(channel)
    pypi_version = version + prerelease_specifiers[channel]

    if pypi_exists(pypi_version):
        print(f"Version {pypi_version} already exists on PyPI. Exiting.")
        sys.exit(0)

    print(f"Using version: {pypi_version}")
    Path(VERSION_FILE).write_text(pypi_version)

    for platform_str, platform_tag in PLATFORMS.items():
        binary_info = next(
            (
                p
                for p in result["downloads"]["chromedriver"]
                if p["platform"] == platform_str
            ),
            None,
        )
        if binary_info is None:
            print(f"No binary found for platform: {platform_str}")
            continue

        url = binary_info["url"]
        print(f"Downloading Chromedriver for platform: {platform_str} from {url}")

        r = requests.get(url, timeout=60)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))

        filename = (
            "chromedriver.exe" if platform_str.startswith("win") else "chromedriver"
        )
        temp_dir = Path("temp_building")
        extract_path = temp_dir / f"chromedriver-{platform_str}"
        target_path = Path("chromedriver_py", filename)

        # Extract, move, and set permissions
        z.extractall(temp_dir)
        (extract_path / filename).rename(target_path)
        shutil.rmtree(temp_dir)
        target_path.chmod(0o755)

        # Build the wheel, specifying the correct platform tag
        print(f"Building wheel for platform: {platform_str}")
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "uv",
                    "build",
                    "--wheel",
                    f"--config-setting=--build-option=--plat-name={platform_tag}",
                ],
            )
        except subprocess.CalledProcessError as e:
            print(f"Error building wheel for {platform_str}: {e}")
            sys.exit(1)

        # cleanup build files
        target_path.unlink()
        Path(VERSION_FILE).unlink()


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in prerelease_specifiers:
        print(
            f"usage: {sys.argv[0]} <channel> (where channel is one of: {', '.join(prerelease_specifiers.keys())})",
        )
        sys.exit(1)
    download_and_build(sys.argv[1])

    print("Build process complete. Wheels are in dist")
