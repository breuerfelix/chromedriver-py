from setuptools import setup


with open('README.md') as f:
    long_description_file = f.read()


with open('version.txt') as f:
    package_version = f.read()


setup(name='chromedriver-py',
      version=package_version,
      description="chromedriver binaries for all platforms",
      long_description=long_description_file,
      long_description_content_type="text/markdown",
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ],
      keywords='chromedriver cross-platform binaries binary',
      url='http://github.com/scriptworld-git/chromedriver-py',
      author='felix.scriptworld',
      author_email='felix@scriptworld.net',
      packages=['chromedriver_py'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
