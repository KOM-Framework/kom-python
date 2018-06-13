import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.drivers import capabilities
from kom_framework.src.web.drivers.drivers import Driver
from kom_framework.src.web.support.web import DriverBase
from ..general import Log
from ..web import hub_ip, hub_port, iframe_load_time, page_load_time


class Browser(DriverBase):

    def __init__(self):
        self.test_session_api = 'http://%s:%s/grid/api/testsession' % (hub_ip, hub_port)

    driver = None

    def get_driver(self, **kwargs) -> WebDriver:
        return Browser.driver

    @staticmethod
    def set_driver(value):
        Browser.driver = value

    def get(self, url: str, extensions: list=()):
        Log.info("Opening %s url" % url)
        if not Browser.driver:
            Log.info("Creating an instance of a Browser.")
            Browser.driver = Driver(extensions).create_session()
        self.get_driver().get(url)

    def switch_to_frame(self, frame_locator: Locator) -> bool:
        out = WebDriverWait(self.get_driver(),
                            iframe_load_time).until(
            expected_conditions.frame_to_be_available_and_switch_to_it(frame_locator))
        return out

    def switch_to_default_content(self):
        self.get_driver().switch_to.default_content()

    def refresh(self):
        Log.info("Refreshing the browser")
        self.get_driver().refresh()
        self.wait_for_page_to_load()

    def refresh_with_accept_browser_alert_if_shown(self):
        Log.info("Refreshing the browser")
        self.accept_browser_alert_if_shown()
        self.get_driver().refresh()
        self.accept_browser_alert_if_shown()
        if capabilities['browserName'] != "internet explorer":
            self.wait_for_page_to_load()

    def accept_browser_alert_if_shown(self):
        try:
            if self.wait_for_alert(1):
                self.accept_alert()
        except TimeoutException:
            pass

    @staticmethod
    def quit():
        if Browser.driver:
            Log.info("Closing the browser")
            try:
                Browser.driver.quit()
            except Exception as e:
                Log.error("Can't quit driver")
                Log.error(e)
            finally:
                Browser.driver = None

    def wait_for_alert(self, wait_time: int=iframe_load_time) -> bool:
        return WebDriverWait(self.get_driver(), wait_time).until(expected_conditions.alert_is_present(),
                                                                 'Timed out waiting for alert to appear.')

    def accept_alert(self):
        Log.info("Accept alert")
        Alert(self.get_driver()).accept()

    def enter_text_into_alert(self, text: str):
        Log.info('Enter "%s" text into Alert' % text)
        Alert(self.get_driver()).send_keys(text)

    def enter_text_and_accept_alert(self, text: str):
        self.wait_for_alert()
        self.enter_text_into_alert(text)
        self.accept_alert()

    def current_url(self):
        return self.get_driver().current_url

    def get_browser_log(self):
        Log.info("Getting browser log")
        logs = self.get_driver().get_log('browser')
        list_logs = list()
        for log_entry in logs:
            log_str = ''
            for key in log_entry.keys():
                log_str += "%s: %s, " % (key, log_entry[key])
            list_logs.append(log_str)
        return list_logs

    def scroll_up(self):
        ActionChains(self.get_driver()).send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.5)

    def scroll_down(self):
        ActionChains(self.get_driver()).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)

    def delete_all_cookies(self):
        self.get_driver().delete_all_cookies()

    def wait_for_page_to_load(self, wait_time: int=page_load_time):
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException:
            Log.info("Page was not loaded in %s seconds" % wait_time)

    def type_keys(self, keys):
        self.get_driver().switch_to.active_element.send_keys(keys)

    def switch_to_last_tab(self):
        Log.info("Browser switch to last tab")
        self.get_driver().switch_to.window(self.get_driver().window_handles[-1])

    def close_last_tab(self):
        Log.info("Browser close last tab")
        if len(self.get_driver().window_handles) > 1:
            self.get_driver().switch_to.window(self.get_driver().window_handles[-1])
            self.get_driver().close()
        self.get_driver().switch_to.window(self.get_driver().window_handles[0])

    def clear_local_storage(self):
        self.get_driver().execute_script('window.localStorage.clear();')

    def execute_script(self, script: str, *args):
        return self.get_driver().execute_script(script, *args)
