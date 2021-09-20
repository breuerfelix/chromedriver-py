# chromedriver-py

downloads and installs the latest chromedriver binary version for automated testing of webapps.  
the installer supports linux, mac and windows operating systems.

this package is maintained by an automated update script on travis.  
if a new chromedriver version is out, this package will automaticly get updated within a day.

## installation

__from pypi:__
```bash
$ pip install chromedriver-py
```

__from github:__
```bash
$ pip install git+https://github.com/breuerfelix/chromedriver-py.git
```

__specific version:__  
choose your version [here](https://pypi.org/project/chromedriver-py/#history)
```bash
# example for chrome version 88
pip install chromedriver-py==88.0.4324.96
```

## usage

to use chromedriver just `from chromedriver_py import binary_path`.  
you will get a string variable with the executable filepath for your operating system.

## example
```python
from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable

driver = webdriver.Chrome(executable_path=binary_path)
driver.get("http://www.python.org")
assert "Python" in driver.title
```

## developer

you can trigger a custom build with a specific version in github actions.  
just click `Run workflow` and put your desired version in the `version` input field that pops up.  
the workflow tries to get your desired version and push it to pypi.
