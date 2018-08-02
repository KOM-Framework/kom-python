from selenium.webdriver.remote.webdriver import WebDriver


def extract_driver_obj(driver):
    if isinstance(driver, WebDriver):
        return driver
    else:
        return driver.parent
