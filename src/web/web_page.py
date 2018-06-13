from abc import ABCMeta, abstractmethod

import time
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.web.browser import Browser
from kom_framework.src.web.data_types import Xpath
from kom_framework.src.web.support.web import DriverBase
from ..general import Log
from ..web import page_load_time
from selenium.webdriver.support import expected_conditions


class WebPage(Browser, DriverBase):

    _retry_count = 0

    def get_driver(self, **kwargs):
        return Browser.driver

    @staticmethod
    def set_driver(value):
        Browser.driver = value

    def __new__(cls, *args, **kwargs):
        obj = super(WebPage, cls).__new__(cls)
        obj.page_name = obj.__class__.__name__
        obj.locator = None
        return obj

    __metaclass__ = ABCMeta

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
                assert self.exists(page_load_time), "Page %s cannot be found" % self.page_name
            self.setup_page()
        except WebDriverException as e:
            if "terminated due to SO_TIMEOUT" in e.msg:
                if self._retry_count <= 1:
                    self._retry_count += 1
                    self.set_driver(None)
                    Log.error('Something went wrong. Retrying to open the page')
                    self.open()
                else:
                    self._retry_count = 0
            raise e
        return self

    def forced_open(self):
        self.quit()
        return self.open()

    def exists(self, wait_time=0) -> bool:
        Log.info("Page '%s' existence verification. Wait time = %s" % (self.page_name, str(wait_time)))
        if self.get_driver():
            try:
                WebDriverWait(self.get_driver(), wait_time).until(
                    expected_conditions.visibility_of_element_located(self.locator)
                )
                return True
            except (NoSuchElementException, TimeoutException):
                Log.info("Page '%s' was not found" % self.page_name)
        return False

    class CanBeFocused:
        def __init__(self, locator):
            self.locator = locator

        def __call__(self, driver):
            try:
                driver.find_element(*self.locator).click()
                return True
            except WebDriverException:
                return False

    def can_be_focused(self, wait: int=15):
        WebDriverWait(self.get_driver(), wait).until(self.CanBeFocused(self.locator))

    def wait_while_text_exists(self, text: str, wait_time: int=30):
        Log.info("Waiting for the '%s' text to disappear" % text)
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                expected_conditions.invisibility_of_element_located((Xpath('//*[contains(text(), "%s")]' % text)))
            )
        except (NoSuchElementException, TimeoutException):
            Log.info("Text '%s' still visible within %s seconds" % (text, wait_time))

    def wait_for_text_exists(self, text: str, wait_time: int=30) -> bool:
        Log.info("Waiting for the '%s' text to appear" % text)
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                expected_conditions.visibility_of_element_located((Xpath('//*[contains(text(), "%s")]' % text)))
            )
            return True
        except (NoSuchElementException, TimeoutException):
            Log.info("Text '%s' was not found in %s seconds" % (text, wait_time))
            return False

    def set_focus(self):
        self.get_driver().find_element(*self.locator).click()

    def text_exists(self, text: str, wait_time: int=0) -> bool:
        Log.info("Text '%s' existence verification. Wait time = %s" % (text, str(wait_time)))
        text_id = (Xpath('//*[contains(text(),"%s")]' % text))
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                expected_conditions.visibility_of_element_located(text_id)
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def check_if_field_is_displayed(self, field_name) -> bool:
        return getattr(self, field_name).is_displayed()

    def wait_while_scrolling(self, wait_time: int=5):
        get_position_command = 'return window.pageYOffset;'
        end_time = time.time() + wait_time
        initial_pos = self.execute_script(get_position_command)
        time.sleep(0.1)
        while True:
            current_pos = self.execute_script(get_position_command)
            if current_pos == initial_pos or time.time() > end_time:
                break
            else:
                initial_pos = current_pos
                time.sleep(0.1)
