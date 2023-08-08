from setuptools import setup

CURRENT_VERSION_FILE = "./CURRENT_VERSION.txt"

with open("README.md") as f:
    long_description_file = f.read()


with open(CURRENT_VERSION_FILE) as f:
    package_version = f.read().strip()


setup(
    name="chromedriver-py",
    version=package_version,
    description="chromedriver binaries for all platforms",
    long_description=long_description_file,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    keywords="chromedriver cross-platform binaries binary",
    url="http://github.com/breuerfelix/chromedriver-py",
    author="Felix Breuer",
    author_email="fbreuer@pm.me",
    packages=["chromedriver_py"],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
