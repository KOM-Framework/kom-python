from kom_framework.src.web.browser import Browser
from kom_framework.src.web.data_types import Name, Id
from kom_framework.src.web.data_types.element_types import Input
from kom_framework.src.web.support.page_factory import find_by
from kom_framework.src.web.web_page import WebPage


class Frame:

    def __init__(self):
        self.lucky = Input(Name("btnI"), action_element=True)


@find_by(Id('viewport'))
class PageTest(WebPage, Frame):

    some_variable = 'SOMETHING NEW'

    def __init__(self):
        Frame.__init__(self)
        self.user = Input(Id("lst-ib"))

    def open_actions(self):
        self.get("http://www.google.com")


class TestSomething:

    def test_decorator(self):
        print(PageTest.some_variable)
        asdasd = Browser()
        asdasd_2 = Browser()
        asdasd.set_driver('valueee')
        print(asdasd_2.get_driver())
        assert True

    def test_action_element(self):
        page = PageTest().open()
        page.lucky.click()
        assert page.exists()

    def test_web_frame(self):
        page = PageTest()
        page.open().lucky.click()
        assert True

    def test_locator(self):
        from kom_framework.src.web.data_types import Xpath
        asda = Xpath('vale')
        print(asda)

    def some_function(self, **kwargs):
        return kwargs

    def test_asdasdasdads(self):
        asdasd = self.some_function(wait_time=0)
        assert True
