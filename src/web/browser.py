import time
from urllib.request import urlopen

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from kom_framework.src.web.drivers.drivers import Driver
from ..general import Log, find_between
from ..web import hub_ip, hub_port, iframe_load_time, http_request_wait_time, \
    page_load_time


class Browser:
    def __init__(self, module_name=None):
        self.driver = None
        self.test_session_api = 'http://%s:%s/grid/api/testsession' % (hub_ip, hub_port)
        self.module_name = module_name

    def get_node_id(self):
        self.open("http://localhost")
        hub_session_api = "%s?session=%s" % (self.test_session_api, self.driver.session_id)
        result = urlopen(hub_session_api)
        string_data = str(result.read())
        Log.info("Result api: %s" % string_data)
        node_id = find_between(string_data, "http://", ":%s" % hub_port)
        Log.info("ProxyId: %s" % node_id)
        self.quit()
        return node_id

    def open(self, url, extensions=None, open_url=True):
        Log.info("Opening %s url" % url)
        if not self.driver:
            Log.info("Creating an instance of a Browser.")
            self.driver = Driver(extensions).create_session()
        if open_url:
            self.driver.get(url)

    def switch_to_frame(self, frame_locator):
        out = WebDriverWait(self.driver,
                            iframe_load_time).until(
            expected_conditions.frame_to_be_available_and_switch_to_it(frame_locator))
        return out

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def wait_until_http_requests_are_finished(self, wait_time=http_request_wait_time):
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: not driver.execute_script("return window.openHTTPs")
            )
        except TimeoutException:
            Log.error('HTTP request execution time is more than %s seconds' % wait_time)
            self.driver.execute_script("window.openHTTPs=0")

    def refresh(self):
        Log.info("Refreshing the browser")
        self.driver.refresh()
        self.wait_for_page_to_load()

    def refresh_with_accept_browser_alert_if_shown(self):
        Log.info("Refreshing the browser")
        self.driver.refresh()
        self.accept_browser_alert_if_shown()
        self.wait_for_page_to_load()

    def accept_browser_alert_if_shown(self):
        if self.wait_for_alert(1):
            self.accept_alert()

    def quit(self):
        if self.driver:
            Log.info("Closing the browser")
            self.driver.quit()
            self.driver = None

    def wait_for_alert(self, wait_time=iframe_load_time):
        return WebDriverWait(self.driver, wait_time).until(expected_conditions.alert_is_present(),
                                                           'Timed out waiting for alert to appear.')

    def accept_alert(self):
        Log.info("Accept alert")
        Alert(self.driver).accept()

    def enter_text_into_alert(self, text):
        Log.info('Enter "%s" text into Alert' % text)
        Alert(self.driver).send_keys(text)

    def enter_text_and_accept_alert(self, text):
        self.wait_for_alert()
        self.enter_text_into_alert(text)
        self.accept_alert()

    def current_url(self):
        return self.driver.current_url

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def get_browser_log(self):
        Log.info("Getting browser log")
        logs = self.driver.get_log('browser')
        list_logs = list()
        for log_entry in logs:
            log_str = ''
            for key in log_entry.keys():
                log_str += "%s: %s, " % (key, log_entry[key])
            list_logs.append(log_str)
        return list_logs

    def scroll_up(self):
        ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.5)

    def scroll_down(self):
        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def wait_for_page_to_load(self, wait_time=page_load_time):
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException:
            Log.info("Page was not loaded in %s seconds" % wait_time)

    def type_keys(self, keys):
        self.driver.switch_to.active_element.send_keys(keys)

    def switch_to_last_tab(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def close_last_tab(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.close()

    def clear_local_storage(self):
        self.driver.execute_script('window.localStorage.clear();')
