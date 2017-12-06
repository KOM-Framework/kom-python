import time

from selenium.webdriver.common.by import By

from kom_framework.src.web.data_types.element import Input
from kom_framework.src.web.web_page import WebPage
from src.integrations.standalone.page_objects import LoginPage


class TestPage(WebPage):

    def __init__(self):
        self.user = Input(By.XPATH, "sdasd")

    def invoke_actions(self):
        pass


class TestFramework:

    def test_01(self):
        page1 = LoginPage("asasd").invoke()
        page3 = LoginPage("assaaaasd").invoke()
        page2 = LoginPage("asdasdaaadaasd").invoke()
        page1.login()
        page2.login()
        page3.login()
        assert True

    def test_02(self):
        start = int(round(time.time() * 1000))
        page = TestPage()
        age2 = TestPage()
        end = int(round(time.time() * 1000))
        print(end-start)
        assert True
