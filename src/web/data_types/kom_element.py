from abc import ABCMeta

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.general import Log
from kom_framework.src.web.data_types.base_element import BaseElement
from kom_framework.src.web.data_types.custom_actions import JSActions, ActionsChains, Waiters
from ...web import element_load_time


class KOMElement(BaseElement, JSActions, ActionsChains, Waiters):

    __metaclass__ = ABCMeta

    def get_driver(self, **kwargs):
        wait_time = kwargs.get('wait_time', 0)
        index = kwargs.get('index', self.ancestor_index)
        out = self.ancestor.get_driver(wait_time=wait_time, index=index)
        return out

    def get_element(self, condition: expected_conditions=presence_of_element_located,
                    wait_time: int=element_load_time) -> WebElement:
        element = WebDriverWait(self.get_driver(wait_time=wait_time), wait_time).until(
            condition(self.locator)
        )
        return element

    def exists(self, wait_time: int=0, condition: expected_conditions=presence_of_element_located) -> bool:
        Log.info("Checking if '%s' element exists" % self.name)
        try:
            self.get_element(condition=condition, wait_time=wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

