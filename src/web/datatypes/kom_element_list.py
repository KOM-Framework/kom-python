from abc import ABCMeta

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ...base_element import KOMElementBase
from ...general import Log
from ...mixins.wait import WaitElementsMixin


class KOMElementList(KOMElementBase):
    __metaclass__ = ABCMeta

    def find(self, wait_time: int = 0):
        return self.wait_for.presence_of_all_elements_located(wait_time)

    @property
    def wait_for(self) -> WaitElementsMixin:
        return WaitElementsMixin(self, self.locator)

    def exists(self, wait_time: int = 0):
        Log.debug("Checking if '%s' list of elements exists" % self.name)
        try:
            return self.find(wait_time)
        except (NoSuchElementException, TimeoutException):
            return False

    @property
    def size(self):
        return len(self.find())

    @property
    def elements_texts(self):
        return [element.text for element in self.find()]

    def select_by_text(self, text: str):
        elements = self.find()
        for element in elements:
            element_text = element.text
            if element_text == text:
                element.click()
                break

    def select_first_enabled(self):
        Log.debug("Selecting first enabled item in the list '%s'" % self.name)
        elements = self.find()
        for item in elements:
            if item.is_enabled():
                item.click()
                break