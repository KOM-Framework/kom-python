from abc import ABCMeta

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ...general import Log
from ...web import element_load_time
from ...web.support.session_factory import WebSessionsFactory


class KOMElement:
    __metaclass__ = ABCMeta

    js_http_requests_listener = "(function() {" \
                                "if (window.httpRequestsListenerStarted) return;" \
                                "window.httpRequestsListenerStarted = true;" \
                                "var oldOpen = XMLHttpRequest.prototype.open;" \
                                "window.openHTTPs = 0;" \
                                "var listener = function(){" \
                                "if (this.readyState == 4) {" \
                                "window.openHTTPs--;" \
                                "this.removeEventListener('readystatechange', listener);" \
                                "}" \
                                "};" \
                                "XMLHttpRequest.prototype.open = function(method, url, async, user, pass){" \
                                "window.openHTTPs++;" \
                                "this.addEventListener('readystatechange', listener);" \
                                "oldOpen.call(this, method, url, async, user, pass);" \
                                "};" \
                                "})();"

    def __new__(cls, *args, **kwargs):
        obj = super(KOMElement, cls).__new__(cls)
        obj.browser_session = WebSessionsFactory.active_page.browser_session
        obj._base_element = WebSessionsFactory.active_frame
        obj.base_element_list = None
        obj.base_element_index = None
        return obj

    def __init__(self, by, value, action_element=False):
        self.__retry_count = 0
        self._locator = (by, value)
        self._name = str(self._locator)
        self._action_element = action_element

    def exists(self, wait_time=0, condition='presence_of_element_located'):
        try:
            self.get_element(condition=condition, wait_time=wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def inject_js_waiter(self):
        self.browser_session.execute_script(KOMElement.js_http_requests_listener)

    def wait_for_all_http_requests_to_be_completed(self):
        self.browser_session.wait_until_http_requests_are_finished()

    def get_element(self, condition='presence_of_element_located', wait_time=element_load_time):
        driver = self.browser_session.driver
        if self.base_element_list:
            driver = self.base_element_list.get_elements()[self.base_element_index]
        elif self._base_element:
            driver = WebDriverWait(driver, wait_time).until(
                expected_conditions.presence_of_element_located(self._base_element._locator))
        element = WebDriverWait(driver, wait_time).until(
            getattr(expected_conditions, condition)(self._locator)
        )
        return element

    def execute_action(self, action, element_condition=None, arg=None):
        if not element_condition:
            element_condition = 'presence_of_element_located'
        obj = getattr(self.get_element(element_condition), action)
        value_type = type(obj).__name__
        if 'str' == value_type:
            self.__retry_count = 0
            return obj
        else:
            try:
                if self._action_element:
                    self.inject_js_waiter()
                if arg is not None:
                    value = obj(arg)
                else:
                    value = obj()
                if self._action_element:
                    self.wait_for_all_http_requests_to_be_completed()
                return value
            except (StaleElementReferenceException, WebDriverException) as e:
                if self.__retry_count <= 2:
                    self.__retry_count += 1
                    Log.error('Error on performing \'%s\' action. Retrying...' % action)
                    Log.error(e.msg)
                    time.sleep(0.5)
                    if 'is not clickable at point' in e.msg:
                        self.scroll_to_element()
                    return self.execute_action(action, element_condition, arg)
                else:
                    self.browser_session.refresh()
                    raise e

    def click(self, expected_element_condition='element_to_be_clickable'):
        self.execute_action('click', expected_element_condition)

    def get_attribute(self, name):
        return self.execute_action('get_attribute', None, name)

    def text(self):
        return self.execute_action("text")

    def move_to(self):
        Log.info("Moving to %s" % self._name)
        ActionChains(self.browser_session.driver).move_to_element(self.get_element()).perform()

    def move_to_and_click(self):
        Log.info("Moving to and clicking on %s" % self._name)
        element = self.get_element()
        ActionChains(self.browser_session.driver).move_to_element(element).click(element).perform()

    def is_displayed(self):
        return self.execute_action('is_displayed')

    def type_keys(self, key):
        Log.info("Typing keys into %s" % self._name)
        self.execute_action('send_keys', None, key)

    def wait_while_exists(self, wait_time=10):
        Log.info('Waiting for the text %s to disappear' % self._name)
        WebDriverWait(self.browser_session.driver, wait_time).until(
            expected_conditions.invisibility_of_element_located(self._locator)
        )

    def wait_for_visibility(self, wait_time=10):
        Log.info('Waiting for the text %s to be visible' % self._name)
        WebDriverWait(self.browser_session.driver, wait_time).until(
            expected_conditions.visibility_of_element_located(self._locator)
        )

    def scroll_to_element(self):
        Log.info("Scrolling to %s element" % self._name)
        self.browser_session.driver.execute_script("return arguments[0].scrollIntoView();", self.get_element())
