import time
from abc import ABCMeta, abstractmethod

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.general import Log
from kom_framework.src.web import http_request_wait_time
from kom_framework.src.web.data_types import Locator


class DriverBase:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_driver(self, **kwargs):
        pass

    def wait_until_http_requests_are_finished(self, wait_time: int=http_request_wait_time):
        try:
            end_time = time.time() + wait_time
            while True:
                if not self.execute_script("return window.openHTTPs") or time.time() > end_time:
                    break
        except TimeoutException:
            Log.error('HTTP request execution time is more than %s seconds' % wait_time)
            self.execute_script("window.openHTTPs=0")

    @staticmethod
    def get_descendant_element(driver, locator: Locator, wait_time: int=0, index: int=0) -> WebElement:
        return WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_all_elements_located(locator))[index]

    @abstractmethod
    def execute_script(self, script: str, *args):
        pass
