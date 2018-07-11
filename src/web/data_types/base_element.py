import time
from abc import abstractmethod

from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, InvalidElementStateException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

from kom_framework.src.general import Log
from kom_framework.src.web import retry_delay
from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.data_types.actions import Action
from kom_framework.src.web.data_types.custom_action_mixins import JsActionMixin
from kom_framework.src.web.support.web import DriverAware


class BaseElement(JsActionMixin):

    @abstractmethod
    def get_driver(self, **kwargs):
        pass

    @abstractmethod
    def exists(self, wait_time: int, condition: expected_conditions) -> bool:
        pass

    def __init__(self, page_object: DriverAware, locator: Locator, action_element: bool=False):
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

    def execute_action(self, action, element_condition: expected_conditions=presence_of_element_located, *args):
        try:
            obj = getattr(self.get_element(element_condition), action)
            if isinstance(obj, str):
                self.__retry_count = 0
                return obj
            else:
                if self.action_element:
                    self.inject_js_waiter()
                if args:
                    value = obj(*args)
                else:
                    value = obj()
                if self.action_element:
                    self.wait_until_http_requests_are_finished()
                return value
        except (StaleElementReferenceException, WebDriverException, InvalidElementStateException) as e:
            if self.__retry_count <= 2:
                self.__retry_count += 1
                Log.error('Error on performing \'%s\' action. Retrying...' % action)
                Log.error(e.msg)
                time.sleep(retry_delay)
                if 'is not clickable at point' in e.msg:
                    self.scroll_to_element()
                return self.execute_action(action, element_condition, *args)
            else:
                raise e

    # Native WebElement methods
    def click(self, expected_element_condition: expected_conditions=element_to_be_clickable):
        self.execute_action(Action.CLICK, expected_element_condition)

    def get_attribute(self, name: str):
        return self.execute_action(Action.GET_ATTRIBUTE, presence_of_element_located, name)

    def text(self) -> str:
        return self.execute_action(Action.TEXT)

    def is_displayed(self) -> bool:
        return self.execute_action(Action.IS_DISPLAYED)

    def type_keys(self, key):
        Log.info("Typing keys into %s" % self.name)
        self.execute_action(Action.SEND_KEYS, presence_of_element_located, key)

    def is_enabled(self) -> bool:
        return self.execute_action(Action.IS_ENABLED)
