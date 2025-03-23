# chromedriver-py

downloads and installs the latest chromedriver binary version for automated testing of webapps.  
the installer supports linux, mac and windows operating systems.

this package is maintained by an automated update script on travis.  
if a new chromedriver version is out, this package will automaticly get updated within a day.

## installation

due to the way how the pipeline packages the binaries, you cannot install the package from github.  
installing from pypi is the only option.

__from pypi:__
```bash
uv add chromedriver-py
```

__specific version:__  
choose your version [here](https://pypi.org/project/chromedriver-py/#history)
```bash
# example for chrome version 88
uv add chromedriver-py==88.0.4324.96
```

## usage

chromedriver will now be located in you system path and will used automatically

## example
```python
from selenium import webdriver

svc = webdriver.ChromeService()  # it will be in the path automatically
driver = webdriver.Chrome(service=svc)

driver.get("http://www.python.org")
assert "Python" in driver.title
```
