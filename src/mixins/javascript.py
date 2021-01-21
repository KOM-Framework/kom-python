import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from kom_framework.src.general import Log
from kom_framework.src.support.driver_aware import DriverAware
from kom_framework.src.web import http_request_wait_time
from kom_framework import js_waiter_file


class JSElementMixin:

    def __init__(self, driver: DriverAware, element: WebElement, element_name: str):
        self.driver = driver
        self.element = element
        self.element_name = element_name

    def execute(self, script, *args) -> str:
        return self.driver.execute_script(script, self.element, *args)

    def inject_waiter(self):
        Log.debug("Injecting JavaScrip HTTP requests waiter into '%s' element" % self.element_name)
        with open(js_waiter_file, 'r') as content:
            js_waiter = content.read()
            self.execute(js_waiter)

    def wait_until_http_requests_are_finished(self, wait_time: int = http_request_wait_time):
        try:
            end_time = time.time() + wait_time
            while True:
                if not self.execute("return window.openHTTPs") or time.time() > end_time:
                    break
        except TimeoutException:
            Log.error('HTTP request execution time is more than %s seconds' % wait_time)
            self.execute("window.openHTTPs=0")

    def scroll_into_view(self):
        Log.info("Scrolling to '%s' element by JavaScript" % self.element_name)
        self.execute("arguments[0].scrollIntoView();")

    def scroll_by(self, x: int, y: int):
        self.execute(f"window.scrollBy({x}, {y});")

    def click(self):
        Log.info("Clicking on '%s' element by JavaScript" % self.element_name)
        self.execute("arguments[0].click();")


class JSBrowserMixin:

    def __init__(self, driver: DriverAware):
        self.driver = driver

    def execute_script(self, script, *args):
        Log.info(f'Executing JS Script: {script}')
        return self.driver.execute_script(script, *args)

    def page_y_offset(self):
        return self.execute_script('return window.pageYOffset;')

    def wait_while_scrolling(self, wait_time: int = 5):
        end_time = time.time() + wait_time
        initial_pos = self.page_y_offset()
        time.sleep(0.1)
        while True:
            current_pos = self.page_y_offset()
            if current_pos == initial_pos or time.time() > end_time:
                break
            else:
                initial_pos = current_pos
                time.sleep(0.1)

    def scroll_down(self, pixels: int = 300):
        """
        Scroll the document down to the vertical position:
        :param pixels: The coordinate to scroll to, along the x-axis (horizontal), in pixels
        :return:
        """
        current_position = self.page_y_offset()
        script = 'window.scrollTo(0, %s);' % str(current_position + pixels)
        return self.execute_script(script)

    def scroll_up(self, pixels: int = 300):
        """
        Scroll the document up to the vertical position:
        :param pixels: The coordinate to scroll to, along the x-axis (horizontal), in pixels
        :return:
        """
        current_position = self.page_y_offset()
        expected_position = str(current_position - pixels)
        script = 'window.scrollTo(0, %s);' % expected_position if expected_position else '0'
        return self.execute_script(script)

    def clear_local_storage(self):
        script = 'window.localStorage.clear();'
        return self.execute_script(script)

    def remove_item_from_local_storage(self, item: str):
        script = f'window.localStorage.removeItem("{item}");'
        return self.execute_script(script)

    def get_local_storage_value_by_key(self, key: str):
        script = f'return window.localStorage.getItem("{key}");'
        return self.execute_script(script)

    def set_local_storage_value_by_key(self, key: str, value: str):
        Log.info(f'Setting local storage item: {key}, {value}')
        script = f'window.localStorage.setItem("{key}", {value});'
        self.execute_script(script)
