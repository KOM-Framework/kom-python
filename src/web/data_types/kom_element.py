from abc import ABCMeta

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    WebDriverException, InvalidElementStateException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ...web.data_types.actions import Action
from ...web.data_types import js_waiter
from ...general import Log
from ...web import element_load_time, retry_delay


class KOMElement:
    __metaclass__ = ABCMeta

    def __init__(self, page_object, locator, action_element=False):
        self.__retry_count = 0
        self.locator = locator
        self._ancestor = page_object
        self._ancestor_index = 0
        self._name = str(locator)
        self._action_element = action_element

    def set_ancestor(self, ancestor):
        self._ancestor = ancestor

    def set_ancestor_index(self, index):
        self._ancestor_index = index

    def exists(self, wait_time=0, condition=expected_conditions.presence_of_all_elements_located):
        Log.info("Checking if %s exists" % self._name)
        try:
            self.get_element(condition=condition, wait_time=wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def inject_js_waiter(self):
        self._ancestor.execute_script(js_waiter)

    def wait_for_all_http_requests_to_be_completed(self):
        self._ancestor.wait_until_http_requests_are_finished()

    def _get_driver(self, wait_time=element_load_time):
        return self._ancestor.get_driver(wait_time=wait_time, index=self._ancestor_index)

    def get_element(self, condition=expected_conditions.presence_of_element_located, wait_time=element_load_time):
        element = WebDriverWait(self._get_driver(wait_time), wait_time).until(
            condition(self.locator)
        )
        return element

    def get_name(self):
        return self._name

    def execute_action(self, action, element_condition=None, arg=None):
        if not element_condition:
            element_condition = expected_conditions.presence_of_element_located
        try:
            obj = getattr(self.get_element(element_condition), action)
            if isinstance(obj, str):
                self.__retry_count = 0
                return obj
            else:
                if self._action_element:
                    self.inject_js_waiter()
                if arg is not None:
                    value = obj(arg)
                else:
                    value = obj()
                if self._action_element:
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

    def click(self, expected_element_condition=expected_conditions.element_to_be_clickable):
        self.execute_action(Action.CLICK, expected_element_condition)

    def drag_and_drop(self, destination):
        Log.info("Drag and Drop on %s" % self._name)
        element = self.get_element()
        if not isinstance(destination, WebElement):
            destination = destination.get_element()
        ActionChains(self._ancestor.driver).drag_and_drop(element, destination).perform()

    def double_click(self):
        Log.info("Double click on %s" % self._name)
        ActionChains(self._ancestor.driver).double_click(self.get_element()).perform()

    def get_attribute(self, name):
        return self.execute_action(Action.GET_ATTRIBUTE, None, name)

    def text(self):
        return self.execute_action(Action.TEXT)

    def move_to(self):
        Log.info("Moving to %s" % self._name)
        ActionChains(self._ancestor.driver).move_to_element(self.get_element()).perform()

    def move_to_and_click(self):
        Log.info("Moving to and clicking on %s" % self._name)
        element = self.get_element()
        ActionChains(self._ancestor.driver).move_to_element(element).click(element).perform()

    def is_displayed(self):
        return self.execute_action(Action.IS_DISPLAYED)

    def type_keys(self, key):
        Log.info("Typing keys into %s" % self._name)
        self.execute_action(Action.SEND_KEYS, None, key)

    def wait_while_exists(self, wait_time=10):
        Log.info('Waiting for the element %s to disappear' % self._name)
        return WebDriverWait(self._get_driver(), wait_time).until(
            expected_conditions.invisibility_of_element_located(self.locator)
        )

    def wait_for_visibility(self, wait_time=10):
        Log.info('Waiting for the element %s to be visible' % self._name)
        return WebDriverWait(self._get_driver(), wait_time).until(
            expected_conditions.visibility_of_element_located(self.locator)
        )

    def wait_for_text_to_be_present_in_element(self, wait_time=5, text=""):
        Log.info('Waiting for the text %s to be present' % self._name)
        x = WebDriverWait(self._get_driver(), wait_time).until(
            expected_conditions.text_to_be_present_in_element(self.locator, text)
        )
        return x

    def scroll_to_element(self):
        Log.info("Scrolling to %s element" % self._name)
        self._ancestor.execute_script("return arguments[0].scrollIntoView();", self.get_element())

    def is_enabled(self):
        return self.execute_action(Action.IS_ENABLED)

    def js_click(self):
        self._ancestor.execute_script("arguments[0].click();", self.get_element())
