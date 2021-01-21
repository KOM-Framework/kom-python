from abc import ABC

from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement

from kom_framework import kom_config
from ..drivers.driver_manager import DriverManager
from ..general import Log
from ..mixins.javascript import JSBrowserMixin
from ..mixins.wait import WaitBrowserMixin
from ..support.driver_aware import DriverAware


class Browser(DriverAware, ABC):

    def __new__(cls, *args, **kwargs):
        obj = super(Browser, cls).__new__(cls)
        obj.__before_instance = list()
        obj.__after_instance = list()
        return obj

    def execute_script(self, script: str, element: WebElement, *args):
        return self.get_driver().execute_script(script, element, *args)

    @property
    def action_chains(self) -> ActionChains:
        return ActionChains(self.get_driver())

    def get_driver(self, wait_time: int = 0):
        return DriverManager.get_session(self)

    def add_before(self, func):
        self.__before_instance.append(func)

    def add_after(self, func):
        self.__after_instance.append(func)

    @property
    def wait_for(self) -> WaitBrowserMixin:
        return WaitBrowserMixin(self)

    @property
    def switch_to(self) -> SwitchTo:
        return SwitchTo(self.get_driver())

    @property
    def alert(self) -> Alert:
        return Alert(self.get_driver())

    @property
    def js(self) -> JSBrowserMixin:
        return JSBrowserMixin(self.get_driver())

    def get(self, url: str, extensions: list = ()):
        Log.info("Opening %s url" % url)
        if not self.get_driver():
            for func in self.__before_instance:
                func()
            DriverManager.create_session(self, extensions)
        self.get_driver().get(url)

    def refresh(self):
        Log.info("Refreshing the browser")
        self.get_driver().refresh()
        self.wait_for.page_is_loaded()

    def current_url(self):
        return self.get_driver().current_url

    def delete_all_cookies(self):
        self.get_driver().delete_all_cookies()

    def window_handles(self):
        return self.get_driver().window_handles

    def close(self):
        self.get_driver().close()

    def quit(self):
        if self.get_driver():
            Log.info("Closing the browser")
            try:
                self.get_driver().quit()
            except Exception:
                pass
            finally:
                DriverManager.destroy_session(self)
                for func in self.__after_instance:
                    func()

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
