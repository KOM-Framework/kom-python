from abc import ABCMeta, abstractmethod

from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

from .browser import Browser
from ..general import Log
from ..support.locators import CssSelector
from ..web import page_load_time
from selenium.webdriver.support import expected_conditions


class PageObject(Browser):
    __metaclass__ = ABCMeta

    _retry_count = 0

    def __new__(cls, *args, **kwargs):
        obj = super(PageObject, cls).__new__(cls)
        obj.page_name = obj.__class__.__name__
        obj.__session_key = f'{obj.page_name}<{str(args)}><{str(kwargs)}>'
        obj.locator = None
        obj.load_time = page_load_time
        return obj

    def find(self, wait_time: int = 0):
        return self.wait_for.condition(wait_time, expected_conditions.presence_of_element_located(self.locator))

    def get_session_key(self):
        return self.__session_key

    def set_session_key(self, key):
        self.__session_key = key

    @abstractmethod
    def open_actions(self):
        pass

    def setup_page(self):
        pass

    def open(self):
        try:
            if not self.exists():
                Log.info("Open %s web page" % self.page_name)
                self.open_actions()
                assert self.exists(self.load_time), "Page %s cannot be found" % self.page_name
            self.setup_page()
        except WebDriverException as e:
            if "terminated due to SO_TIMEOUT" in e.msg:
                if self._retry_count <= 1:
                    self._retry_count += 1
                    Log.error('Something went wrong. Retrying to open the page')
                    self.open()
                else:
                    self._retry_count = 0
            raise e
        return self

    def reopen(self):
        self.quit()
        return self.open()

    def exists(self, wait_time: int = 0) -> bool:
        Log.info("Page '%s' existence verification. Wait time = %s" % (self.page_name, str(wait_time)))
        if self.get_driver():
            try:
                self.wait_for.condition(wait_time, expected_conditions.visibility_of_element_located(self.locator))
                return True
            except (NoSuchElementException, TimeoutException):
                Log.info("Page '%s' was not found" % self.page_name)
        return False

    def disappears(self, wait_time: int = 0) -> bool:
        Log.info("Page '%s' disappearance verification. Wait time = %s" % (self.page_name, str(wait_time)))
        if self.get_driver():
            try:
                self.wait_for.condition(wait_time, expected_conditions.invisibility_of_element_located(self.locator))
                return True
            except (NoSuchElementException, TimeoutException, WebDriverException) as e:
                if e.msg == 'TypeError: can\'t access dead object':
                    # FF workaround https://github.com/mozilla/geckodriver/issues/614
                    return True
                Log.info("Page '%s' did not disappear" % self.page_name)
        return False

    def can_be_focused(self, wait_time: int = page_load_time):
        self.wait_for.condition(wait_time, expected_conditions.element_to_be_clickable(self.locator))

    def wait_while_text_exists(self, text: str, wait_time: int = 30):
        Log.info("Waiting for the '%s' text to disappear" % text)
        try:
            self.wait_for.condition(wait_time, expected_conditions.text_to_be_present_in_element(CssSelector('*'),
                                                                                                 text))
        except (NoSuchElementException, TimeoutException):
            Log.info("Text '%s' still visible within %s seconds" % (text, wait_time))

    def wait_for_text_exists(self, text: str, wait_time: int = 30) -> bool:
        Log.info("Waiting for the '%s' text to appear" % text)
        try:
            self.wait_for.condition(wait_time, expected_conditions.text_to_be_present_in_element(CssSelector('*'),
                                                                                                 text))
            return True
        except (NoSuchElementException, TimeoutException):
            Log.info("Text '%s' was not found in %s seconds" % (text, wait_time))
            return False

    def set_focus(self):
        self.wait_for.condition(0, expected_conditions.element_to_be_clickable(self.locator)).click()

    def field_is_displayed(self, field_name) -> bool:
        return getattr(self, field_name).is_displayed()
