from abc import ABCMeta

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    WebDriverException, NoSuchFrameException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.general import Log
from kom_framework.src.web import element_load_time
from kom_framework.src.web.support.session_factory import WebSessionsFactory


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
        obj.__retry_count = 0
        obj.browser_session = WebSessionsFactory.active_page.browser_session
        obj._base_element = WebSessionsFactory.active_frame
        obj.base_element_list = None
        obj.base_element_index = None
        return obj

    def __init__(self, by, value):
        self._locator = (by, value)
        self._name = str(self._locator)

    def exists(self, wait_time=0, condition='presence_of_element_located'):
        try:
            self.get_element(condition=condition, wait_time=wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

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
        try:
            obj = getattr(self.get_element(element_condition), action)
            value_type = type(obj).__name__
            if 'str' == value_type:
                self.__retry_count = 0
                return obj
            else:
                if arg is not None:
                    value = obj(arg)
                else:
                    value = obj()
                self.__retry_count = 0
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
        self.browser_session.execute_script(KOMElement.js_http_requests_listener)
        self.execute_action('click', expected_element_condition)
        self.browser_session.wait_until_http_requests_are_finished()

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


class Input(KOMElement):
    def send_keys(self, value):
        Log.info("Sending %s keys to the '%s' input field" % (value, self._name))
        self.browser_session.execute_script(KOMElement.js_http_requests_listener)
        self.execute_action('send_keys', 'element_to_be_clickable', str(value))
        self.browser_session.wait_until_http_requests_are_finished()

    def clear_and_send_keys(self, value, use_action_chain=False):
        Log.info("Clearing and sending %s keys to the '%s' input field" % (value, self._name))
        if use_action_chain:
            ActionChains(self.browser_session.driver).click(self.get_element()) \
                .send_keys(Keys.DELETE) \
                .send_keys(Keys.BACKSPACE) \
                .perform()
            self.execute_action('send_keys', 'element_to_be_clickable', str(value))
        else:
            self.execute_action('clear', 'element_to_be_clickable')
            self.execute_action('send_keys', 'element_to_be_clickable', str(value))

    def clear(self):
        Log.info("Clearing %s input field" % self._name)
        self.execute_action('clear')

    def type_keys(self, value):
        Log.info("Typing %s keys to the '%s' input field" % (value, self._name))
        element = self.get_element('element_to_be_clickable')
        for ch in str(value):
            element.send_keys(ch)
            time.sleep(0.1)

    def send_keys_to_invisible_field(self, value):
        Log.info("Sending %s keys '%s' to the invisible text field" % (value, self._name))
        self.browser_session.execute_script(KOMElement.js_http_requests_listener)
        self.execute_action('send_keys',  arg=str(value))
        self.browser_session.wait_until_http_requests_are_finished()

    def get_content(self):
        return self.execute_action("get_attribute", arg="value")


class FRInput(Input):

    def get_content(self):
        return self.execute_action("text")


class TextBlock(KOMElement):
    def text(self):
        Log.info("Getting text from the '%s' text block" % self._name)
        return super(TextBlock, self).text()


class Button(KOMElement):
    def click(self, **kwargs):
        Log.info("Clicking on the '%s' button" % self._name)
        super(Button, self).click(**kwargs)


class PanelItem(KOMElement):
    def click(self, **kwargs):
        Log.info("Clicking on the '%s' panel item" % self._name)
        super(PanelItem, self).click(**kwargs)


class LinkedText(KOMElement):

    def text(self):
        Log.info("Getting text from the '%s' linked text" % self._name)
        return super(LinkedText, self).text()


class Link(KOMElement):

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' web link" % self._name)
        super(Link, self).click(**kwargs)


class CheckBox(KOMElement):

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' check box" % self._name)
        super(CheckBox, self).click(**kwargs)

    def check(self, value=True):
        Log.info("Checking the '%s' check box" % self._name)
        actual_status = super(CheckBox, self).get_attribute('value')
        if (value and actual_status != 'true') or (not value and actual_status == 'true'):
            super(CheckBox, self).click()


class MultiSelectTree(KOMElement):

    def __init__(self, field_by, field_value, select_area, option_list, added_item, delete_item):
        super().__init__(field_by, field_value)
        self._select_area = select_area
        self._option_list = option_list
        self._added_item = added_item
        self._delete_item = delete_item

    def add_item(self, option_name):
        Log.info("Adding %s item to the %s" % (option_name, self._name))
        field = self.get_element()
        field.find_element_by_xpath(self._select_area).click()
        options = field.find_elements_by_xpath(self._option_list)
        for option in options:
            if option.text == option_name:
                option.click()
                break
        field.find_element_by_xpath(self._select_area).click()

    def get_selected_items(self):
        Log.info("Getting all the added items to the %s" % self._name)
        field = self.get_element()
        time.sleep(1)
        items = field.find_elements_by_xpath(self._added_item)
        out = [item.text for item in items]
        return out

    def delete_item(self, item_name):
        Log.info("Deleting %s item to the %s" % (item_name, self._name))
        field = self.get_element()
        time.sleep(1)
        item_index = self.get_selected_items().index(item_name)
        if item_index:
            element = field.find_element_by_xpath('%s[%s]%s' % (self._added_item, str(item_index+1), self._delete_item))
            element.click()


class IFrame(KOMElement):

    def switch_to(self):
        Log.info("Switching to iFrame: '%s'" % self._name)
        self.browser_session.switch_to_frame(self._locator)

    def exists(self, wait_time=5, **kwargs):
        Log.info("Checking if %s frame exists" % self._name)
        try:
            WebDriverWait(self.browser_session.driver,
                          wait_time).until(
                expected_conditions.frame_to_be_available_and_switch_to_it(self._locator))
            self.browser_session.switch_to_default_content()
            return True
        except NoSuchFrameException:
            return False


class Image(KOMElement):
    pass
