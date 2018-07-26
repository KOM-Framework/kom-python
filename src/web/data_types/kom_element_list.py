from abc import ABCMeta

from copy import copy

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from kom_framework.src.web.data_types.base_element import BaseElement
from kom_framework.src.web.mixins.wait import WaitElementsMixin
from ...general import Log


class Structure(dict):

    __getattr__, __setattr__ = dict.get, dict.__setitem__

    def get_copy(self):
        keys = self.keys()
        out = dict()
        for key in keys:
            out[key] = copy(self[key])
        return Structure(out)

    def init_structure(self, ancestor, length: int, index: int):
        out = list()
        field_names = self.keys()
        for i in range(length):
            if index is not None:
                i = index
            obj = self.get_copy()
            for field in field_names:
                field_object = getattr(obj, field)
                field_object.set_ancestor(ancestor)
                field_object.set_ancestor_index(i)
            if index is not None:
                return obj
            out.append(obj)
        return out


class KOMElementList(BaseElement):

    __metaclass__ = ABCMeta

    def find(self, wait_time: int=0):
        return self.wait_for().presence_of_all_elements_located(wait_time)

    def wait_for(self) -> WaitElementsMixin:
        return WaitElementsMixin(self.get_driver(), self.locator)

    def exists(self, wait_time: int=0):
        Log.info("Checking if '%s' list of elements exists" % self.name)
        try:
            self.wait_for().presence_of_all_elements_located(wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def get_size(self):
        return len(self.wait_for().presence_of_all_elements_located())

    def select_first_enabled(self):
        Log.info("Selecting first enabled item in the list '%s'" % self.name)
        elements = self.wait_for().presence_of_all_elements_located()
        for item in elements:
            if item.is_enabled():
                item.click()
                break

    def get_elements_texts(self):
        return [element.text for element in self.wait_for().presence_of_all_elements_located()]
