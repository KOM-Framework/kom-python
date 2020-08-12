from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from kom_framework.src.drivers.window_drivers import AppiumDriver
from kom_framework.src.general import Log
from kom_framework.src.mixins.actions import Actions
from kom_framework.src.mixins.wait import WaitElementMixin
from kom_framework.src.support.driver_aware import DriverAware
from kom_framework.src.web import appium_platform


class WindowObject(DriverAware):

    def find(self, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        obj = super(WindowObject, cls).__new__(cls)
        obj.name = obj.__class__.__name__
        obj.__session = None
        obj.locator = None
        obj.load_time = 5
        return obj

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, value):
        self.__session = value

    def execute_script(self, script: str, element: WebElement, *args):
        pass

    @property
    def wait_for(self) -> WaitElementMixin:
        return WaitElementMixin(self.get_driver(), self.locator)

    @property
    def action_chains(self) -> Actions:
        return Actions(self.get_driver())

    def get_driver(self, wait_time: int = 0):
        if not self.session:
            Log.debug(f"Creating an instance of a {appium_platform} driver.")  # TODO: Move driver name to a config
            self.session = AppiumDriver.get_remote_session()
        return self.session

    def exists(self, wait_time: int = 0):
        Log.debug(f"Window '{self.name}' existence verification. Wait time = {str(wait_time)}")
        if self.get_driver():
            try:
                self.wait_for.visibility_of_element_located(self.load_time)
                return True
            except (NoSuchElementException, TimeoutException):
                Log.debug("Window '%s' was not found" % self.name)
        return False

    def quit(self):
        if self.get_driver():
            Log.debug("Closing the Appium driver session")
            try:
                self.get_driver().quit()
            except Exception as e:
                Log.error("Can't quit Appium driver")
                Log.error(e)
            finally:
                self.session = None
