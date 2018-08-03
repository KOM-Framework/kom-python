from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.switch_to import SwitchTo

from kom_framework.src.web.mixins.java_script import JSBrowserMixin
from kom_framework.src.web.mixins.wait import WaitBrowserMixin
from kom_framework.src.web.drivers.drivers import Driver
from kom_framework.src.web.support.web import DriverAware
from ..general import Log


class Browser(DriverAware):

    __driver = None

    def find(self, **kwargs):
        pass

    @staticmethod
    def get_driver() -> WebDriver:
        return Browser.__driver

    @staticmethod
    def set_driver(value):
        Browser.__driver = value

    def wait_for(self) -> WaitBrowserMixin:
        return WaitBrowserMixin(self.get_driver())

    def switch_to(self) -> SwitchTo:
        return SwitchTo(self.get_driver())

    def alert(self) -> Alert:
        return Alert(self.get_driver())

    def js(self) -> JSBrowserMixin:
        return JSBrowserMixin(self.get_driver())

    def get(self, url: str, extensions: list=()):
        Log.info("Opening %s url" % url)
        if not self.get_driver():
            Log.info("Creating an instance of a Browser.")
            self.set_driver(Driver(extensions).create_session())
        self.get_driver().get(url)

    def refresh(self):
        Log.info("Refreshing the browser")
        self.get_driver().refresh()
        self.wait_for().page_is_loaded()

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
            except Exception as e:
                Log.error("Can't quit driver")
                Log.error(e)
            finally:
                self.set_driver(None)

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
