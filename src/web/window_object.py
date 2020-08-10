import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from kom_framework import kom_config
from kom_framework.src.general import Log
from kom_framework.src.web.data_types import Xpath
from kom_framework.src.web.drivers.driver_manager import DriverManager
from kom_framework.src.web.mixins.wait import NoSuchElementException, WaitElementMixin


from kom_framework.src.web.data_types.base_element import KOMElementBase
from kom_framework.src.web.support.web import DriverAware


class Button(KOMElementBase):

    def exists(self, wait_time: int) -> bool:
        pass

    def get_driver(self, wait_time: int = 0):
        driver = self.ancestor.get_driver(wait_time)
        return driver

    @property
    def wait_for(self) -> WaitElementMixin:
        absolute_locator = self.ancestor.locator.value + self.locator.value
        return WaitElementMixin(self.ancestor, Xpath(absolute_locator))

    def find(self, wait_time: int = 2):
        return self.wait_for.presence_of_element_located(wait_time)

    def click(self):
        self.find().click()


class WindowFactory:

    @classmethod
    def init_elements(cls, instance: DriverAware, ancestor: DriverAware):
        elements = vars(instance)
        for element_name in elements:
            element_object = elements[element_name]
            if isinstance(element_object, KOMElementBase):
                element_object.ancestor = ancestor


def find_by(locator: Xpath):
    def real_decorator(class_):
        class WrapperMeta(type):
            def __getattr__(self, attr):
                return getattr(class_, attr)

        class Wrapper(metaclass=WrapperMeta):
            def __new__(cls, *args, **kwargs):
                win_object = class_(*args, **kwargs)
                win_object.locator = locator
                WindowFactory.init_elements(win_object, win_object)
                return win_object

        return Wrapper

    return real_decorator


class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: time.sleep(time_s))
        return self


class WindowObject(DriverAware):

    def __new__(cls, *args, **kwargs):
        obj = super(WindowObject, cls).__new__(cls)
        obj.name = obj.__class__.__name__
        obj.__session_key = f'{obj.name}<{str(args)}><{str(kwargs)}>'
        obj.locator = None
        obj.load_time = 5
        return obj

    def get_session_key(self):
        return self.__session_key

    def set_session_key(self, key):
        self.__session_key = key

    def execute_script(self, script: str, element: WebElement, *args):
        pass

    @property
    def wait_for(self) -> WaitElementMixin:
        return WaitElementMixin(self.get_driver(), self.locator)

    @property
    def action_chains(self) -> Actions:
        return Actions(self.get_driver())

    def get_driver(self, wait_time: int = 0):
        Log.debug(f"Creating an instance of a {kom_config['driver_configurations']['browserName']} driver.")
        DriverManager.create_session(self, None)
        return DriverManager.get_session(self)

    def exists(self, wait_time: int = 0):
        Log.debug(f"Window '{self.name}' existence verification. Wait time = {str(wait_time)}")
        if self.get_driver():
            try:
                self.wait_for.visibility_of_element_located(self.load_time)
                return True
            except (NoSuchElementException, TimeoutException):
                Log.debug("Window '%s' was not found" % self.name)
        return False

    def find(self, **kwargs):
        pass
