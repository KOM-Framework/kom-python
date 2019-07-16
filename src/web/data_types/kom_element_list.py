from abc import ABCMeta


from selenium.common.exceptions import NoSuchElementException, TimeoutException

from kom_framework.src.web.data_types.base_element import KOMElementBase
from kom_framework.src.web.mixins.wait import WaitElementsMixin
from ...general import Log


class KOMElementList(KOMElementBase):

    __metaclass__ = ABCMeta

    def find(self, wait_time: int=0):
        return self.wait_for.presence_of_all_elements_located(wait_time)

    @property
    def wait_for(self) -> WaitElementsMixin:
        return WaitElementsMixin(self, self.locator)

    def exists(self, wait_time: int=0):
        Log.info("Checking if '%s' list of elements exists" % self.name)
        try:
            return self.find()
        except (NoSuchElementException, TimeoutException):
            return False

    @property
    def size(self):
        return len(self.find())

    @property
    def elements_texts(self):
        return [element.text for element in self.find()]

    def select_first_enabled(self):
        Log.info("Selecting first enabled item in the list '%s'" % self.name)
        elements = self.find()
        for item in elements:
            if item.is_enabled():
                item.click()
                break
