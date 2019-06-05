from abc import ABC

from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement

from kom_framework.src.web.drivers.driver_manager import DriverManager
from kom_framework.src.web.mixins.javascript import JSBrowserMixin
from kom_framework.src.web.mixins.wait import WaitBrowserMixin
from kom_framework.src.web.support.web import DriverAware
from ..general import Log


class Browser(DriverAware, ABC):

    def __new__(cls, *args, **kwargs):
        obj = super(Browser, cls).__new__(cls)
        obj.__before_instance = list()
        obj.__after_instance = list()
        return obj

    def execute_script(self, script: str, element: WebElement, *args):
        return self.driver.execute_script(script, element, *args)

    @property
    def action_chains(self) -> ActionChains:
        return ActionChains(self.driver)

    @property
    def driver(self):
        return DriverManager.get_session(self)

    def add_before(self, func):
        self.__before_instance.append(func)

    def add_after(self, func):
        self.__after_instance.append(func)

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

    def get(self, url: str, extensions: list = ()):
        Log.info("Opening %s url" % url)
        if not self.driver:
            Log.info("Creating an instance of a Browser.")
            for func in self.__before_instance:
                func()
            DriverManager.create_session(self, extensions)
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
                DriverManager.destroy_session(self)
                for func in self.__after_instance:
                    func()

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
