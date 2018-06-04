from abc import abstractmethod

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.web import page_load_time
from ..general import Log
from ..web.support.helper import WebPageHelper
from selenium.webdriver.support import expected_conditions


class WebFrame(WebPageHelper):

    def get_driver(self, **kwargs):
        wait_time = kwargs.get('wait_time', 0)
        index = kwargs.get('index', 0)
        return self.get_descendant_element(self._ancestor.get_driver(), self.locator, wait_time, index)

    def __new__(cls, *args, **kwargs):
        obj = super(WebFrame, cls).__new__(cls)
        obj.frame_name = obj.__class__.__name__
        obj.locator = None
        return obj

    def __init__(self, ancestor):
        self._ancestor = ancestor

    def exists(self, wait_time=0):
        Log.info("Frame '%s' existence verification. Wait time = %s" % (self.frame_name, str(wait_time)))
        if self._ancestor.get_driver():
            try:
                WebDriverWait(self._ancestor.get_driver(), wait_time).until(
                    expected_conditions.visibility_of_element_located(self.locator)
                )
                return True
            except (NoSuchElementException, TimeoutException):
                Log.info("Frame '%s' was not found" % self.frame_name)
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

    def execute_script(self, script, *args):
        return self._ancestor.execute_script(script, *args)

    def quit(self):
        self._ancestor.quit()
