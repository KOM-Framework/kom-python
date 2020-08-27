import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait, POLL_FREQUENCY

from kom_framework.src.general import Log
from kom_framework.src.support.driver_aware import DriverAware
from kom_framework.src.support.locators import Locator
from kom_framework.src.web import element_load_time, page_load_time


class WaitMixin:

    def __init__(self, driver: DriverAware):
        self.driver = driver

    def condition(self, wait_time: int, condition: expected_conditions, poll_frequency: float = POLL_FREQUENCY,
                  ignored_exceptions: list = None):
        try:
            if isinstance(self.driver, DriverAware):
                driver = self.driver.get_driver(wait_time)
            else:
                driver = self.driver
            return WebDriverWait(driver, wait_time, poll_frequency, ignored_exceptions).until(condition)
        except StaleElementReferenceException:
            time.sleep(poll_frequency)
            wait_time -= poll_frequency
            return self.condition(wait_time, condition, poll_frequency, ignored_exceptions)


class WaitElementMixin(WaitMixin):

    def __init__(self, driver: DriverAware, element_locator: Locator):
        super().__init__(driver)
        self.locator = element_locator
        self.name = str(self.locator)

    def presence_of_element_located(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                    ignored_exceptions=None):
        Log.info('An expectation for checking that an element "%s" is present on the DOM of a page.' % self.name)
        return self.condition(wait_time, presence_of_element_located(self.locator), poll_frequency, ignored_exceptions)

    def visibility_of_element_located(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                      ignored_exceptions=None):
        Log.info('An expectation for checking that an element "%s" is present on the DOM of a page and visible.'
                 % self.name)
        return self.condition(wait_time, visibility_of_element_located(self.locator), poll_frequency,
                              ignored_exceptions)

    def visibility_of(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                      ignored_exceptions=None):
        Log.info('Waiting for the existing "%s" element on the page to be visible.' % self.name)
        return self.condition(wait_time, visibility_of(self.presence_of_element_located()), poll_frequency,
                              ignored_exceptions)

    def text_to_be_present_in_element(self, text: str, wait_time: int = element_load_time,
                                      poll_frequency=POLL_FREQUENCY,
                                      ignored_exceptions=None):
        Log.info('Checking if the given text is present in the specified element "%s".' % self.name)
        return self.condition(wait_time, text_to_be_present_in_element(self.locator, text), poll_frequency,
                              ignored_exceptions)

    def text_to_be_present_in_element_value(self, text: str, wait_time: int = element_load_time,
                                            poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        Log.info('Checking if the given text is present in the element\'s locator "%s", text.' % self.name)
        return self.condition(wait_time, text_to_be_present_in_element_value(self.locator, text), poll_frequency,
                              ignored_exceptions)

    def invisibility_of_element_located(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                        ignored_exceptions=None):
        Log.info('An Expectation for checking that an element "%s" is either invisible or not present on the DOM.'
                 % self.name)
        return self.condition(wait_time, invisibility_of_element_located(self.locator), poll_frequency,
                              ignored_exceptions)

    def element_to_be_clickable(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                ignored_exceptions=None):
        Log.info('An Expectation for checking an element "%s" is visible and enabled such that you can click it.'
                 % self.name)
        return self.condition(wait_time, element_to_be_clickable(self.locator), poll_frequency, ignored_exceptions)

    def staleness_of(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                     ignored_exceptions=None):
        Log.info('Wait until an element is no longer attached to the DOM. "%s" is the element to wait for' % self.name)
        return self.condition(wait_time, staleness_of(self.presence_of_element_located()), poll_frequency,
                              ignored_exceptions)

    def element_to_be_selected(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                               ignored_exceptions=None):
        Log.info('An expectation for checking the selection "%s" is selected.' % self.name)
        return self.condition(wait_time, element_to_be_selected(self.presence_of_element_located()), poll_frequency,
                              ignored_exceptions)

    def element_located_to_be_selected(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                       ignored_exceptions=None):
        Log.info('An expectation for the element "%s" to be located is selected.' % self.name)
        return self.condition(wait_time, element_located_to_be_selected(self.locator), poll_frequency,
                              ignored_exceptions)

    def element_selection_state_to_be(self, is_selected: bool, wait_time: int = element_load_time,
                                      poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        Log.info('An expectation for checking if the given element "%s" is selected.' % self.name)
        return self.condition(wait_time, element_selection_state_to_be(self.presence_of_element_located(), is_selected),
                              poll_frequency, ignored_exceptions)

    def element_located_selection_state_to_be(self, is_selected: bool, wait_time: int = element_load_time,
                                              poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        Log.info('An expectation to locate an element "%s" and check if the selection state specified is in that '
                 'state.' % self.name)
        return self.condition(wait_time, element_selection_state_to_be(self.locator, is_selected), poll_frequency,
                              ignored_exceptions)


class WaitElementsMixin(WaitMixin):

    def __init__(self, driver: DriverAware, element_locator: Locator):
        super().__init__(driver)
        self.locator = element_locator
        self.name = str(self.locator)

    def presence_of_all_elements_located(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                         ignored_exceptions=None):
        Log.info('An expectation for checking that there is at least one element "%s" present on a web page.'
                 % self.name)
        return self.condition(wait_time, presence_of_all_elements_located(self.locator), poll_frequency,
                              ignored_exceptions)

    def visibility_of_any_elements_located(self, wait_time: int = element_load_time, poll_frequency=0.5,
                                           ignored_exceptions=None):
        Log.info('An expectation for checking that there is at least one element "%s" visible on a web page.'
                 % self.name)
        return self.condition(wait_time, visibility_of_any_elements_located(self.locator), poll_frequency,
                              ignored_exceptions)

    def visibility_of_all_elements_located(self, wait_time: int = element_load_time, poll_frequency=0.5,
                                           ignored_exceptions=None):
        Log.info('An expectation for checking that all elements "%s" are present on the DOM of a page and visible.'
                 % self.name)
        return self.condition(wait_time, visibility_of_all_elements_located(self.locator), poll_frequency,
                              ignored_exceptions)

    def number_of_elements(self, elements_count: int, wait_time: int = element_load_time, poll_frequency=0.5,
                           ignored_exceptions=None):
        Log.info('An expectation for checking that number elements "%s" are present on the DOM of a page.'
                 % self.name)
        return self.condition(wait_time, lambda driver: len(driver.find_elements(*self.locator)) == elements_count,
                              poll_frequency, ignored_exceptions)


class WaitBrowserMixin(WaitMixin):

    def __init__(self, driver: DriverAware):
        super().__init__(driver)

    def title_is(self, title: str, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                 ignored_exceptions=None):
        Log.info('An expectation for checking the title of a page.')
        return self.condition(wait_time, title_is(title), poll_frequency, ignored_exceptions)

    def title_contains(self, title: str, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                       ignored_exceptions=None):
        Log.info('An expectation for checking that the title contains a case-sensitive substring.')
        return self.condition(wait_time, title_contains(title), poll_frequency, ignored_exceptions)

    def url_contains(self, url: str, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                     ignored_exceptions=None):
        Log.info('An expectation for checking that the current url contains a case-sensitive substring.')
        return self.condition(wait_time, url_contains(url), poll_frequency, ignored_exceptions)

    def url_matches(self, pattern: str, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                    ignored_exceptions=None):
        Log.info('An expectation for checking the current url.')
        return self.condition(wait_time, url_matches(pattern), poll_frequency, ignored_exceptions)

    def url_to_be(self, url: str, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                  ignored_exceptions=None):
        Log.info('An expectation for checking the current url.')
        return self.condition(wait_time, url_to_be(url), poll_frequency, ignored_exceptions)

    def url_changes(self, url: str, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                    ignored_exceptions=None):
        Log.info('An expectation for checking the current url.')
        return self.condition(wait_time, url_changes(url), poll_frequency, ignored_exceptions)

    def frame_to_be_available_and_switch_to_it(self, locator: Locator, wait_time: int = page_load_time,
                                               poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        Log.info('An expectation for checking whether the given frame "%s" is available to switch to.' % str(locator))
        return self.condition(wait_time, frame_to_be_available_and_switch_to_it(locator),
                              poll_frequency, ignored_exceptions)

    def number_of_windows_to_be(self, num_windows: int, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                                ignored_exceptions=None):
        Log.info('An expectation for the number of windows to be a certain value.')
        return self.condition(wait_time, number_of_windows_to_be(num_windows), poll_frequency,
                              ignored_exceptions)

    def new_window_is_opened(self, current_handles: list, wait_time: int = page_load_time,
                             poll_frequency=POLL_FREQUENCY,
                             ignored_exceptions=None):
        Log.info('An expectation that a new window will be opened and have the number of windows handles increase')
        return self.condition(wait_time, new_window_is_opened(current_handles), poll_frequency,
                              ignored_exceptions)

    def alert_is_present(self, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                         ignored_exceptions=None):
        Log.info('Expect an alert to be present.')
        return self.condition(wait_time, alert_is_present(), poll_frequency, ignored_exceptions)

    def page_is_loaded(self, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                       ignored_exceptions=None):
        self.condition(wait_time, lambda driver: driver.execute_script('return document.readyState') == 'complete',
                       poll_frequency, ignored_exceptions)
