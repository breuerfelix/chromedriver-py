from selenium import webdriver

svc = webdriver.ChromeService()
driver = webdriver.Chrome(service=svc)
driver.get("http://www.python.org")
assert "Python" in driver.title
