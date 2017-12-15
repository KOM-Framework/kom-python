from selenium.webdriver.common.by import By

from kom_framework.src.web.data_types.element_types import Input
from kom_framework.src.web.support.page_factory import locator
from kom_framework.src.web.web_page import WebPage


@locator(By.ID, 'viewport')
class TestPage(WebPage):

    def __init__(self, module_name=None):
        self._set_module(module_name)
        self.user = Input(By.ID, "lst-ib")

    def open_actions(self):
        self.browser_session.open("http://www.google.com")


class TestFramework:

    def test_01(self):
        TestPage("module_1").open()
        TestPage("module_2").open()
        assert True

    def test_02(self):
        page = TestPage()
        age2 = TestPage()
        assert True
