import os
import sys
import urllib
import zipfile
import requests
from bs4 import BeautifulSoup as bs

# constants
CHROMEDRIVER_URL = "https://chromedriver.storage.googleapis.com/"
PLATFORMS = [
    "linux64",
    "win32",
    "mac64",
    "mac64_m1",
]
CHROMEDRIVER_FILE_NAME = "chromedriver_"
CHROMEDRIVER_EXTENSION = ".zip"

DOWNLOAD_DIR = "./chromedriver_py/"
VERSION_FILE = "./CURRENT_VERSION.txt"


def compare_int_arrays(old, new):
    shortest = old if len(old) < len(new) else new

    for i in range(len(shortest)):
        if new[i] == old[i]:
            continue

        if new[i] > old[i]:
            return True

        break

    return False


def check_for_update(old_version_param=None):
    if not old_version_param:
        old_version_param = "0.0"

    old_version = []
    try:
        old_version_param = old_version_param.split(".")
        for v in old_version_param:
            old_version.append(int(v))
    except:
        print("error parsing old version!")
        return None, None

    print("old version: " + str(old_version))

    page = requests.get(CHROMEDRIVER_URL)
    html = page.content

    soup = bs(html, "lxml")

    versions_to_update = set()
    checked_keys = []

    highest_version = []

    for content in soup.select("contents"):
        key = content.select("key")
        if not key:
            # key not found
            continue

        key = key[0]
        key = key.get_text()

        version = key.split("/")

        # key is not a version
        if not version:
            continue

        version = version[0]

        # continue if version is already checked
        if version in checked_keys:
            continue

        checked_keys.append(version)

        version_list = version.split(".")

        # key is no version either
        if not version_list:
            print("no valid version key: " + version)
            continue

        # try parse version to int
        versions = []
        for v in version_list:
            try:
                versions.append(int(v))
            except:
                print("failed parsing to version number: " + version)
                versions = []
                break

        # continue if version number got non-int
        if not versions:
            continue

        if compare_int_arrays(old_version, versions):
            versions_to_update.add(".".join(str(x) for x in versions))

            # check for highest possible version
            if not highest_version:
                highest_version = versions
            elif compare_int_arrays(highest_version, versions):
                highest_version = versions

    highest_version = ".".join(str(x) for x in highest_version)

    print("versions to update: " + str(versions_to_update))
    print("highest version to update: " + highest_version)

    return highest_version, versions_to_update


def update_version(version):
    for p in PLATFORMS:
        filename = CHROMEDRIVER_FILE_NAME + p
        filename_version = version + "/" + filename + CHROMEDRIVER_EXTENSION
        url = CHROMEDRIVER_URL + filename_version
        print(url)

        # downloads the files
        try:
            file = urllib.request.urlopen(url)
        except:
            print("could not get file: " + filename)
            continue

        # save file to system
        path = os.path.join(DOWNLOAD_DIR, filename + CHROMEDRIVER_EXTENSION)
        with open(path, "wb") as output:
            print("write to: " + path)
            output.write(file.read())

        # unzip file
        print("unzip file: " + path)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

        # rename file
        extracted_name = "chromedriver"
        if p == "win":
            extracted_name += ".exe"
            filename += ".exe"

        print("rename file to: " + filename)
        final_path = os.path.join(DOWNLOAD_DIR, filename)
        os.rename(os.path.join(DOWNLOAD_DIR, extracted_name), final_path)

        # give execute permission
        print("setting permissions")
        os.chmod(final_path, 0o755)

        # delete zip file
        print("removing file: " + path)
        os.remove(path)

    return version


def get_version_from_file(path):
    try:
        with open(path, "r") as f:
            current_version = f.read().strip()

        return current_version
    except:
        pass

    return None


if __name__ == "__main__":
    # get environment version for custom travis builds
    env_version = os.environ.get("VERSION")

    if not env_version:
        current_version = get_version_from_file(VERSION_FILE)
        print("current version: " + str(current_version))

        version, _ = check_for_update(current_version)

        if not version:
            # exit with code 1 to prevent auto deploy
            sys.exit(1)
    else:
        print("got version from environment: " + env_version)
        version = env_version

    version = update_version(version)
    print("version updated: " + version)

    # update version file
    with open(VERSION_FILE, "w") as f:
        # only write the major and minor version to file
        f.write(version)

    # exit with code 0 to enable auto-deploy
    sys.exit(0)
