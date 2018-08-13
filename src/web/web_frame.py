from abc import abstractmethod

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from kom_framework.src.web import page_load_time
from kom_framework.src.web.mixins.wait import WaitElementMixin
from kom_framework.src.web.support.web import DriverAware
from ..general import Log


class WebFrame(DriverAware):

    def __new__(cls, *args, **kwargs):
        obj = super(WebFrame, cls).__new__(cls)
        obj.frame_name = obj.__class__.__name__
        obj.locator = None
        return obj

    def __init__(self, ancestor):
        self.ancestor = ancestor

    @property
    def driver(self):
        return self.ancestor.find()

    def find(self, wait_time: int = 0):
        return self.wait_for.presence_of_element_located(wait_time)

    @property
    def wait_for(self) -> WaitElementMixin:
        return WaitElementMixin(self.driver, self.locator)

    def exists(self, wait_time: int=0) -> bool:
        Log.info("Frame '%s' existence verification. Wait time = %s" % (self.frame_name, str(wait_time)))
        if self.ancestor.driver:
            try:
                self.wait_for.visibility_of_element_located(wait_time)
                return True
            except (NoSuchElementException, TimeoutException):
                Log.info("Frame '%s' was not found" % self.frame_name)
        return False

    def wait_to_disappear(self, wait_time: int=0):
        Log.info("Waiting for the Frame '%s' to disappear. Wait time = %s" % (self.frame_name, str(wait_time)))
        try:
            self.wait_for.invisibility_of_element_located(wait_time)
            return True
        except TimeoutException:
            Log.info("Frame '%s' was still found" % self.frame_name)
        return False

    @abstractmethod
    def open_actions(self):
        pass

    def setup_frame(self):
        pass

    def open(self):
        if not self.exists():
            Log.info("Open %s web frame" % self.frame_name)
            self.open_actions()
            assert self.exists(page_load_time), "Frame %s cannot be found" % self.frame_name
        if "setup_frame" in dir(self):
            self.setup_frame()
        return self

    def quit(self):
        self.ancestor.quit()

    def execute_script(self, script: str, *args):
        element = self.driver
        element.parent.execute_script(script, element, *args)
