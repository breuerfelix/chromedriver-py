from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable

driver = webdriver.Chrome(executable_path = binary_path)
driver.get("http://www.python.org")
assert "Python" in driver.title
