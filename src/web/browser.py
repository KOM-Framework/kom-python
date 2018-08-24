from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement

from kom_framework.src.web.mixins.javascript import JSBrowserMixin
from kom_framework.src.web.mixins.wait import WaitBrowserMixin
from kom_framework.src.web.drivers.drivers import Driver
from kom_framework.src.web.support.web import DriverAware
from ..general import Log


class Browser(DriverAware):

    __driver = None

    def find(self, **kwargs):
        pass

    def execute_script(self, script: str, element: WebElement, *args):
        return self.driver.execute_script(script, element, *args)

    @property
    def action_chains(self) -> ActionChains:
        return ActionChains(self.driver)

    @property
    def driver(self):
        return Browser.__driver

    @driver.setter
    def driver(self, driver):
        Browser.__driver = driver

    @property
    def wait_for(self) -> WaitBrowserMixin:
        return WaitBrowserMixin(self.driver)

    @property
    def switch_to(self) -> SwitchTo:
        return SwitchTo(self.driver)

    @property
    def alert(self) -> Alert:
        return Alert(self.driver)

    @property
    def js(self) -> JSBrowserMixin:
        return JSBrowserMixin(self.driver)

    def get(self, url: str, extensions: list=()):
        Log.info("Opening %s url" % url)
        if not self.driver:
            Log.info("Creating an instance of a Browser.")
            self.driver = Driver(extensions).create_session()
        self.driver.get(url)

    def refresh(self):
        Log.info("Refreshing the browser")
        self.driver.refresh()
        self.wait_for.page_is_loaded()

    def current_url(self):
        return self.driver.current_url

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def window_handles(self):
        return self.driver.window_handles

    def close(self):
        self.driver.close()

    def quit(self):
        if self.driver:
            Log.info("Closing the browser")
            try:
                self.driver.quit()
            except Exception as e:
                Log.error("Can't quit driver")
                Log.error(e)
            finally:
                self.driver = None

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
