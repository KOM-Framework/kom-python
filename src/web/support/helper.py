from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.general import Log
from kom_framework.src.web import http_request_wait_time


class WebPageHelper:

    def get_driver(self, **kwargs):
        pass

    def execute_script(self, script, *args):
        return self.get_driver().execute_script(script, *args)

    def wait_until_http_requests_are_finished(self, wait_time=http_request_wait_time):
        try:
            WebDriverWait(self.get_driver(), wait_time).until(
                lambda driver: not driver.execute_script("return window.openHTTPs")
            )
        except TimeoutException:
            Log.error('HTTP request execution time is more than %s seconds' % wait_time)
            self.get_driver().execute_script("window.openHTTPs=0")

    @staticmethod
    def get_descendant_element(driver, locator, wait_time=0, index=0):
        return WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_all_elements_located(locator))[index]
