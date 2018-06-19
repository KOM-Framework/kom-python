import time
from abc import abstractmethod

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.general import Log
from kom_framework.src.web import element_load_time
from kom_framework.src.web.data_types import js_waiter
from selenium.webdriver import ActionChains


class JSActions:

    @property
    def name(self):
        raise NotImplementedError

    @property
    def ancestor(self):
        raise NotImplementedError

    @abstractmethod
    def get_element(self):
        pass

    def execute_script(self, script, *args):
        element = self.get_element()
        element.parent.execute_script(script, element, *args)

    def inject_js_waiter(self):
        Log.info("Injecting JavaScrip HTTP requests waiter into '%s' element" % self.name)
        self.execute_script(js_waiter)

    def wait_for_all_http_requests_to_be_completed(self):
        self.ancestor.wait_until_http_requests_are_finished()

    def scroll_to_element(self):
        Log.info("Scrolling to '%s' element by JavaScript" % self.name)
        self.execute_script("arguments[0].scrollIntoView();")

    def js_click(self):
        Log.info("Clicking on '%s' element by JavaScript" % self.name)
        self.execute_script("arguments[0].click();")


class ActionsChains:

    @abstractmethod
    def get_element(self):
        pass

    @property
    def name(self):
        raise NotImplementedError

    def drag_and_drop(self, destination):
        Log.info("Drag and Drop on %s" % self.name)
        element = self.get_element()
        if not isinstance(destination, WebElement):
            destination = destination.get_element()
        ActionChains(element.parent).drag_and_drop(element, destination).perform()

    def double_click(self):
        Log.info("Double click on %s" % self.name)
        element = self.get_element()
        ActionChains(element.parent).double_click(element).perform()

    def move_to(self):
        Log.info("Moving to %s" % self.name)
        element = self.get_element()
        ActionChains(element.parent).move_to_element(element).perform()

    def move_to_and_click(self):
        Log.info("Moving to and clicking on %s" % self.name)
        element = self.get_element()
        ActionChains(element.parent).move_to_element(element).click(element).perform()


class Waiters:

    @property
    def name(self):
        raise NotImplementedError

    @property
    def locator(self):
        raise NotImplementedError

    @abstractmethod
    def text(self) -> str:
        pass

    @abstractmethod
    def get_element(self):
        pass

    def wait_while_exists(self, wait_time: int=10):
        Log.info('Waiting for the element %s to disappear' % self.name)
        return WebDriverWait(self.get_element().parent, wait_time).until(
            expected_conditions.invisibility_of_element_located(self.locator)
        )

    def wait_for_visibility(self, wait_time: int=10):
        Log.info('Waiting for the element %s to be visible' % self.name)
        return WebDriverWait(self.get_element().parent, wait_time).until(
            expected_conditions.visibility_of_element_located(self.locator)
        )

    def wait_for_text_to_be_present_in_element(self, wait_time: int=element_load_time, text: str=""):
        Log.info('Waiting for the text %s to be present' % self.name)
        x = WebDriverWait(self.get_element().parent, wait_time).until(
            expected_conditions.text_to_be_present_in_element(self.locator, text)
        )
        return x

    def wait_for_value(self, expected_value: str, wait_time: int=5) -> str:
        end_time = time.time() + wait_time
        while True:
            actual_value = self.text()
            if actual_value == expected_value or time.time() > end_time:
                break
        return actual_value
