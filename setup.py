from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='chromedriver-py',
      version='0.1',
      description=readme(),
      long_description='Really, the funniest around.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='chromedriver cross-platform binaries binary',
      url='http://github.com/scriptworld-git/chromedriver-py',
      author='felix.scriptworld',
      author_email='felix@scriptworld.net',
      license='MIT',
      packages=['chromedriver-py'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
