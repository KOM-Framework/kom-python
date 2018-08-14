from abc import abstractmethod

from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.support.web import DriverAware


class BaseElement(DriverAware):

    def get_driver(self, wait_time: int=0):
        driver = self.ancestor.find(wait_time=wait_time)
        if self.ancestor_index is not None:
            return driver[self.ancestor_index]
        return driver

    @abstractmethod
    def exists(self, wait_time: int) -> bool:
        pass

    def __init__(self, page_object: DriverAware, locator: Locator, ancestor_index: int=None, action_element: bool=False):
        self._retry_count = 0
        self.__locator = locator
        self.__ancestor = page_object
        self.__ancestor_index = ancestor_index
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

    @property
    def ancestor_index(self):
        return self.__ancestor_index

    @property
    def action_element(self):
        return self.__action_element
