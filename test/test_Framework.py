from selenium.webdriver.common.by import By

from kom_framework.src.web.data_types.element_types import Input
from kom_framework.src.web.support.page_factory import locator
from kom_framework.src.web.web_page import WebPage


@locator(By.ID, 'viewport')
class PageTest(WebPage):

    some_variable = 'SOMETHING NEW'

    def __init__(self, module_name=None):
        self._set_module(module_name)
        self.user = Input(By.ID, "lst-ib")
        self.lucky = Input(By.NAME, "btnI", action_element=True)

    def open_actions(self):
        self.browser_session.open("http://www.google.com")


class TestSomething:

    def test_decorator(self):
        print(PageTest.some_variable)
        obj_1 = PageTest('asdasd')
        obj_2 = PageTest('asdasdass')
        obj_3 = PageTest('asdasd')
        assert True

    def test_session_factory_close(self):
        from kom_framework.src.web.support.session_factory import WebSessionsFactory
        obj_1 = PageTest('asdasd').open()
        obj_2 = PageTest('asdasda2ss').open()
        WebSessionsFactory.close_sessions()
        assert True

    def test_action_element(self):
        page = PageTest().open()
        page.lucky.click()
        assert page


