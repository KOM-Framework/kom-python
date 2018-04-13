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


class KOMElementList(KOMElement):
    __metaclass__ = ABCMeta

    def get_elements(self):
        return WebDriverWait(self.get_driver(), element_load_time).until(
            expected_conditions.presence_of_all_elements_located(self.locator)
        )

    def exists(self, wait_time=0, **kwargs):
        Log.info("List '%s' existence verification. Wait time = %s" % (self._name, str(wait_time)))
        try:
            WebDriverWait(self.browser_session.driver, wait_time).until(
                lambda driver: driver.find_elements(*self.locator)
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def select_first_enabled(self):
        Log.info("Selecting first enabled item in the list '%s'" % self._name)
        elements = self.get_elements()
        for item in elements:
            if item.is_enabled():
                item.click()
                break
