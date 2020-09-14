from selenium.common.exceptions import TimeoutException

from kom_framework.src.base_element import KOMElementBase
from kom_framework.src.mixins.wait import WaitElementMixin
from kom_framework.src.support.locators import Xpath


class Button(KOMElementBase):

    def exists(self, wait_time: int = 0) -> bool:
        try:
            self.wait_for.visibility_of_element_located(wait_time)
            return True
        except TimeoutException:
            return False

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
