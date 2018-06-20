import time
from abc import ABCMeta, abstractmethod

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.general import Log
from kom_framework.src.web import http_request_wait_time
from kom_framework.src.web.data_types import Locator


class Ancestor:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_driver(self, **kwargs):
        pass

    @staticmethod
    def get_descendant_element(driver, locator: Locator, wait_time: int=0) -> WebElement:
        element = WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_element_located(locator))
        return element

    @abstractmethod
    def execute_script(self, script: str, *args):
        pass
