from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from kom_framework.src.mixins.wait import WaitElementsMixin
from kom_framework.src.support.driver_aware import DriverAware
from kom_framework.src.web.page_factory import PageFactory


class Components(DriverAware):

    def get_driver(self, wait_time: int = 0):
        return self.__ancestor.find()

    def __new__(cls, *args, **kwargs):
        obj = super(Components, cls).__new__(cls)
        obj.frame_name = obj.__class__.__name__
        obj.locator = None
        return obj

    def __init__(self, ancestor):
        self.__ancestor = ancestor

    @property
    def ancestor(self):
        return self.__ancestor

    def find(self, wait_time: int = 0):
        return self.wait_for.presence_of_all_elements_located(wait_time)

    @property
    def action_chains(self) -> ActionChains:
        return self.__ancestor.action_chains

    def execute_script(self, script: str, element: WebElement, *args):
        self.__ancestor.execute_script(script, element, *args)

    @property
    def wait_for(self) -> WaitElementsMixin:
        return WaitElementsMixin(self.get_driver(), self.locator)

    def exists(self, wait_time: int = 0):
        try:
            return self.find(wait_time)
        except (NoSuchElementException, TimeoutException):
            return False

    def get_content(self, wait_time: int = 0):
        out = []
        if self.exists(wait_time):
            elements = self.find()
            for ancestor_index in range(len(elements)):
                structure_object = self.__class__(self.ancestor)
                PageFactory.init_elements(structure_object, self, ancestor_index)
                out.append(structure_object)
        return out
