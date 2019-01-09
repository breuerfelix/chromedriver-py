# chromedriver-py

downloads and installs the latest chromedriver binary version for automated testing of webapps.  
the installer supports linux, mac and windows operating systems.

this package is maintained by an automated update script on travis.  
if a new chromedriver version is out, this package will automaticly get updated within a day.

## installation

__from pypi__  
```bash
$ pip install chromedriver-py
```

__from github__
```bash
$ pip install git+https://github.com/scriptworld-git/chromedriver-py.git
```

## usage

to use chromedriver just `from chromedriver_py import binary_path`.  
you will get a string variable with the excecutable filepath for your operating system.

## example
```python
from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable

driver = webdriver.Chrome(executabel_path=binary_path)
driver.get("http://www.python.org")
assert "Python" in driver.title
```
