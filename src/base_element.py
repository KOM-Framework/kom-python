from abc import abstractmethod

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from kom_framework.src.support.driver_aware import DriverAware
from kom_framework.src.support.locators import Locator


class KOMElementBase(DriverAware):

    def __init__(self, locator: Locator, action_element: bool = False):
        self._retry_count = 0
        self.__locator = locator
        self.__name = str(locator)
        self.__action_element = action_element
        self.__ancestor = None
        self.__ancestor_index = None

    def get_driver(self, wait_time: int = 0):
        driver = self.ancestor.find(wait_time)
        if self.ancestor_index is not None:
            return driver[self.ancestor_index]
        return driver

    @abstractmethod
    def exists(self, wait_time: int) -> bool:
        pass

    def execute_script(self, script: str, element: WebElement, *args):
        self.ancestor.execute_script(script, element, *args)

    def action_chains(self) -> ActionChains:
        return self.ancestor.action_chains

    @property
    def locator(self):
        return self.__locator

    @property
    def name(self):
        return self.__name

    @property
    def ancestor(self):
        return self.__ancestor

    @ancestor.setter
    def ancestor(self, value: DriverAware):
        self.__ancestor = value

    @property
    def ancestor_index(self):
        return self.__ancestor_index

    @ancestor_index.setter
    def ancestor_index(self, value):
        self.__ancestor_index = value

    @property
    def action_element(self):
        return self.__action_element
