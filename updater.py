from typing import Literal, TypeAlias, cast
import requests
import zipfile
import io
import os
import sys

URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
PLATFORMS = [
    'linux64',
    'mac-arm64',
    'mac-x64',
    'win32',
    'win64',
]
VERSION_FILE = "CURRENT_VERSION.txt"

Channel: TypeAlias = Literal["Canary", "Dev", "Beta", "Stable"]

prerelease_specifiers: dict[Channel, str] = {
    "Stable": "",
    "Beta": "b",
    "Dev": "a",
    "Canary": ".dev"
}

def fetch_latest_version(channel: Channel):
    result = requests.get(URL).json()["channels"][channel]
    return result["version"], result

def pypi_exists(version):
    url = f"https://pypi.org/pypi/chromedriver-py/{version}/json"
    response = requests.get(url)
    return response.status_code == 200


def download_binaries(channel):
    for p in channel["downloads"]["chromedriver"]:
        platform = p["platform"]
        url = p["url"]
        print(f"platform: {platform}")

        print("downloading zip file")
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))

        path = f"chromedriver-{platform}"
        origin = os.path.join(path, "chromedriver")
        dest = os.path.join("chromedriver_py", f"chromedriver_{platform}")

        if platform.startswith("win"):
            origin += ".exe"
            dest += ".exe"

        print("extracting zip file")
        z.extract(origin.replace("\\", "/"))

        print("moving file to correct folder")
        os.rename(origin, dest)

        # give execute permission
        print("setting permissions")
        os.chmod(dest, 0o755)

        # delete zip folder
        print("removing file: " + path)
        os.removedirs(path)


if __name__ == "__main__":
    channel = cast(Channel, sys.argv[1])
    version, result = fetch_latest_version(channel)
    pypi_version = version + prerelease_specifiers[channel]
    if pypi_exists(pypi_version):
        sys.exit(0)

    print(f"using version: {version}")
    download_binaries(result)

    with open(VERSION_FILE, "w") as f:
        f.write(pypi_version)
