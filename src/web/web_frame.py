from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from ..general import Log
from ..web.support.session_factory import WebSessionsFactory
from selenium.webdriver.support import expected_conditions


class WebFrame:

    def __new__(cls, *args, **kwargs):
        obj = super(WebFrame, cls).__new__(cls)
        obj.frame_name = obj.__class__.__name__
        obj.module_name = obj.__class__.__module__
        obj.browser_session = WebSessionsFactory.browser(obj.module_name)
        WebSessionsFactory.active_frame = obj
        return obj

    def exists(self, wait_time=0):
        Log.info("Frame '%s' existence verification. Wait time = %s" % (self.frame_name, str(wait_time)))
        if self.browser_session.driver:
            try:
                WebDriverWait(self.browser_session.driver, wait_time).until(
                    expected_conditions.visibility_of_element_located(getattr(self, "_locator"))
                )
                return True
            except (NoSuchElementException, TimeoutException):
                Log.info("Frame '%s' was not found" % self.frame_name)
        return False
