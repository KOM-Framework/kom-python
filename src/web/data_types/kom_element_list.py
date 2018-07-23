from abc import ABCMeta

from copy import copy
from typing import List

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, \
    visibility_of_any_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.web.data_types.base_element import BaseElement
from kom_framework.src.web.data_types.kom_element import KOMElement
from ...general import Log
from ...web import element_load_time


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

    def get_driver(self, **kwargs):
        wait_time = kwargs.get('wait_time', 0)
        index = kwargs.get('index', self.ancestor_index)
        out = self.get_element(wait_time=wait_time)[index]
        return out

    def get_element(self, condition: expected_conditions=presence_of_all_elements_located,
                    wait_time: int=element_load_time) -> List[KOMElement]:
        elements = WebDriverWait(self.ancestor.get_driver(wait_time=wait_time), wait_time).until(
            condition(self.locator)
        )
        kom_elements = list()
        for i in range(elements):
            kom_element = KOMElement(self.ancestor, self.locator)
            kom_element.set_ancestor_index(i)
            kom_elements.append(kom_element)
        return kom_elements

    def exists(self, wait_time: int=0, condition: expected_conditions=presence_of_all_elements_located):
        Log.info("Checking if '%s' list of elements exists" % self.name)
        try:
            self.get_element(condition=condition, wait_time=wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def get_size(self):
        return len(self.get_element())

    def select_first_enabled(self):
        Log.info("Selecting first enabled item in the list '%s'" % self.name)
        elements = self.get_element()
        for item in elements:
            if item.is_enabled():
                item.click()
                break

    def get_elements_texts(self):
        return [element.text for element in self.get_element()]

    def wait_for_visibility(self, wait_time=element_load_time):
        Log.info('Waiting for the grid %s to be visible' % self.name)
        self.get_element(condition=visibility_of_any_elements_located, wait_time=wait_time)

    def wait_for_elements_count(self, elements_count, wait_time):
        Log.info('Waiting for the %s elements appears in a grid %s' % (elements_count, self.name))
        try:
            WebDriverWait(self.ancestor.get_driver(), wait_time).until(
                lambda driver: len(driver.find_elements(*self.locator)) == elements_count)
            return True
        except TimeoutException:
            return False
