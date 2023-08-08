import requests
import zipfile
import io
import os

URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
PLATFORMS = [
    'linux64',
    'mac-arm64',
    'mac-x64',
    'win32',
    'win64',
]
VERSION_FILE = "CURRENT_VERSION.txt"

def download_url(version, platform, binary):
    return f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/{platform}/{binary}-{platform}.zip"

def fetch_latest_version():
    return requests.get(URL).json()["channels"]["Stable"]["version"]

def download_binaries(version):
    for platform in PLATFORMS:
        print(f"platform: {platform}")

        print("downloading zip file")
        url = download_url(version, platform, "chromedriver")
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))

        path = f"chromedriver-{platform}"
        origin = os.path.join(path, "chromedriver")
        dest = os.path.join("chromedriver_py", f"chromedriver_{platform}")

        if platform.startswith("win"):
            origin += ".exe"
            dest += ".exe"

        print("extracting zip file")
        z.extract(origin)

        print("moving file to correct folder")
        os.rename(origin, dest)

        # give execute permission
        print("setting permissions")
        os.chmod(dest, 0o755)

        # delete zip folder
        print("removing file: " + path)
        os.removedirs(path)


if __name__ == "__main__":
    version = os.getenv("VERSION")
    if not version:
        version = fetch_latest_version()

    print(f"using version: {version}")
    download_binaries(version)

    with open(VERSION_FILE, "w") as f:
        f.write(version)
