from abc import ABCMeta

from copy import copy

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ...web.data_types.kom_element import KOMElement
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


class KOMElementList(KOMElement):
    __metaclass__ = ABCMeta

    def get_elements(self, wait_time=element_load_time):
        return WebDriverWait(self.get_driver(), wait_time).until(
            expected_conditions.presence_of_all_elements_located(self.locator)
        )

    def get_size(self):
        return len(self.get_elements())

    def exists(self, wait_time=0, **kwargs):
        Log.info("List '%s' existence verification. Wait time = %s" % (self.name, str(wait_time)))
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                lambda driver: driver.find_elements(*self.locator)
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def select_first_enabled(self):
        Log.info("Selecting first enabled item in the list '%s'" % self.name)
        elements = self.get_elements()
        for item in elements:
            if item.is_enabled():
                item.click()
                break

    def get_elements_texts(self):
        return [element.text for element in self.get_elements()]

    def wait_for_visibility(self, wait_time=element_load_time):
        Log.info('Waiting for the grid %s to be visible' % self.name)
        WebDriverWait(self.get_driver(), wait_time).until(
            expected_conditions.presence_of_all_elements_located(self.locator)
        )

    def wait_for_elements_count(self, elements_count, wait_time):
        Log.info('Waiting for the %s elements appears in a grid %s' % (elements_count, self.name))
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                lambda driver: len(driver.find_elements(*self.locator)) == elements_count)
            return True
        except TimeoutException:
            return False
