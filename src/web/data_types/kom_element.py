from abc import ABCMeta

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    WebDriverException, InvalidElementStateException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.web.data_types.custom_actions import JSActions, ActionsChains, Waiters
from kom_framework.src.web.support.web import DriverBase
from ...web.data_types.actions import Action
from ...web.data_types import Locator
from ...general import Log
from ...web import element_load_time, retry_delay


class KOMElement(WebElement, JSActions, ActionsChains, Waiters):

    __metaclass__ = ABCMeta

    def __init__(self, page_object: DriverBase, locator: Locator, action_element: bool=False):
        super().__init__(page_object, Locator)
        self.__retry_count = 0
        self.__locator = locator
        self.__ancestor = page_object
        self.__ancestor_index = 0
        self.__name = str(locator)
        self.__action_element = action_element

    @property
    def locator(self):
        return self.__locator

    @property
    def name(self):
        return self.__name

    @property
    def ancestor(self):
        return self.__ancestor

    @property
    def ancestor_index(self):
        return self.__ancestor_index

    @property
    def action_element(self):
        return self.__action_element

    def set_ancestor(self, ancestor):
        self.__ancestor = ancestor

    def set_ancestor_index(self, index: int):
        self.__ancestor_index = index

    def get_driver(self, wait_time: int=element_load_time):
        return self.ancestor.get_driver(wait_time=wait_time, index=self.ancestor_index)

    def get_element(self, condition=expected_conditions.presence_of_element_located, wait_time: int=element_load_time)\
            -> WebElement:
        element = WebDriverWait(self.get_driver(wait_time), wait_time).until(
            condition(self.locator)
        )
        return element

    def execute_action(self, action, element_condition=None, arg=None):
        if not element_condition:
            element_condition = expected_conditions.presence_of_element_located
        try:
            obj = getattr(self.get_element(element_condition), action)
            if isinstance(obj, str):
                self.__retry_count = 0
                return obj
            else:
                if self.action_element:
                    self.inject_js_waiter()
                if arg is not None:
                    value = obj(arg)
                else:
                    value = obj()
                if self.action_element:
                    self.wait_for_all_http_requests_to_be_completed()
                return value
        except (StaleElementReferenceException, WebDriverException, InvalidElementStateException) as e:
            if self.__retry_count <= 2:
                self.__retry_count += 1
                Log.error('Error on performing \'%s\' action. Retrying...' % action)
                Log.error(e.msg)
                time.sleep(retry_delay)
                if 'is not clickable at point' in e.msg:
                    self.scroll_to_element()
                return self.execute_action(action, element_condition, arg)
            else:
                raise e

    def exists(self, wait_time: int=0, condition=expected_conditions.presence_of_all_elements_located):
        Log.info("Checking if %s exists" % self.name)
        try:
            self.get_element(condition=condition, wait_time=wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    # Native WebElement methods
    def click(self, expected_element_condition=expected_conditions.element_to_be_clickable):
        self.execute_action(Action.CLICK, expected_element_condition)

    def get_attribute(self, name: str):
        return self.execute_action(Action.GET_ATTRIBUTE, None, name)

    def text(self):
        return self.execute_action(Action.TEXT)

    def is_displayed(self):
        return self.execute_action(Action.IS_DISPLAYED)

    def type_keys(self, key):
        Log.info("Typing keys into %s" % self.name)
        self.execute_action(Action.SEND_KEYS, None, key)

    def is_enabled(self):
        return self.execute_action(Action.IS_ENABLED)
