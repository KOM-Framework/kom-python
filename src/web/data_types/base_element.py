from abc import abstractmethod

from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.support.web import DriverAware


class BaseElement(DriverAware):

    @property
    def driver(self):
        driver = self.ancestor.find()
        if self.ancestor_index is not None:
            return driver[self.ancestor_index]
        return driver

    @abstractmethod
    def exists(self, wait_time: int) -> bool:
        pass

    def __init__(self, page_object: DriverAware, locator: Locator, action_element: bool=False):
        self._retry_count = 0
        self.__locator = locator
        self.__ancestor = page_object
        self.__ancestor_index = None
        self.__name = str(locator)
        self.__action_element = action_element

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
    def ancestor(self, ancestor):
        self.__ancestor = ancestor

    @property
    def ancestor_index(self):
        return self.__ancestor_index

    @ancestor_index.setter
    def ancestor_index(self, index: int):
        self.__ancestor_index = index

    @property
    def action_element(self):
        return self.__action_element
