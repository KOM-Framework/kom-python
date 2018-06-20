import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.support.web import Ancestor
from ...general import Log
from ...web.data_types.actions import Action
from ...web.data_types.kom_element import KOMElement


class Input(KOMElement):
    """
      Prefix it with inp_
    """

    def __init__(self, page_object: Ancestor, locator: Locator, message_locator: Locator=None, **kwargs):
        KOMElement.__init__(self, page_object, locator, **kwargs)
        self.message_locator = message_locator

    def clear(self, use_action_chain: bool=False):
        Log.info("Clearing %s input field" % self.name)
        if use_action_chain:
            element = self.get_element()
            ActionChains(element.parent).click(element) \
                .send_keys(Keys.END) \
                .key_down(Keys.SHIFT) \
                .send_keys(Keys.HOME) \
                .key_up(Keys.SHIFT) \
                .send_keys(Keys.DELETE) \
                .perform()
        else:
            self.execute_action(Action.CLEAR)

    def send_keys(self, value: str):
        Log.info("Sending %s keys to the '%s' input field" % (value, self.name))
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, value)

    def clear_and_send_keys(self, value: str, use_action_chain: bool=False):
        Log.info("Clearing and sending %s keys to the '%s' input field" % (value, self.name))
        self.clear(use_action_chain)
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, value)

    def type_keys(self, value: str):
        Log.info("Typing %s keys to the '%s' input field" % (value, self.name))
        element = self.get_element(expected_conditions.element_to_be_clickable)
        for ch in value:
            element.send_keys(ch)
            time.sleep(0.1)

    def send_keys_to_invisible_field(self, value: str):
        Log.info("Sending %s keys '%s' to the invisible text field" % (value, self.name))
        self.execute_action(Action.SEND_KEYS, presence_of_element_located, value)

    def get_content(self) -> str:
        return self.execute_action(Action.GET_ATTRIBUTE, presence_of_element_located, "value")

    def get_message(self) -> str:
        if self.message_locator:
            message = AnyType(self.ancestor, self.message_locator)
            if message.exists():
                return message.text()
        else:
            raise Exception('Input message locator is not defined')
        return ""


class FRInput(Input):

    def get_content(self) -> str:
        return self.execute_action(Action.TEXT)


class TextBlock(KOMElement):
    """
        Prefix it with txt_
    """

    def text(self) -> str:
        Log.info("Getting text from the '%s' text block" % self.name)
        return super(TextBlock, self).text()


class TextArea(KOMElement):
    """
        Prefix it with txa_
    """

    def text(self) -> str:
        Log.info("Getting text from the '%s' text area" % self.name)
        return super(TextArea, self).text()


class Button(KOMElement):
    """
        Prefix it with btn_
    """

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' button" % self.name)
        super(Button, self).click(**kwargs)


class PanelItem(KOMElement):
    """
        Prefix with pnl_
    """

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' panel item" % self.name)
        super(PanelItem, self).click(**kwargs)


class LinkedText(KOMElement):
    """
        Prefix with lkt_
    """

    def text(self):
        Log.info("Getting text from the '%s' linked text" % self.name)
        return super(LinkedText, self).text()


class Link(KOMElement):
    """
        Prefix it with lnk_
    """

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' web link" % self.name)
        super(Link, self).click(**kwargs)


class CheckBox(KOMElement):
    """
        Prefix with chk_
    """

    def __init__(self, ancestor: Ancestor, locator: Locator, attribute: str='value', checked_value: str='on', **kwargs):
        KOMElement.__init__(self, ancestor, locator, **kwargs)
        self.attribute = attribute
        self.checked_value = checked_value

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' check box" % self.name)
        super(CheckBox, self).click(**kwargs)

    def check(self, value: bool=True):
        Log.info("Checking the '%s' check box" % self.name)
        actual_status = super(CheckBox, self).get_attribute(self.attribute)
        if (value and actual_status != self.checked_value) or (not value and actual_status == self.checked_value):
            super(CheckBox, self).click()

    def is_selected(self) -> bool:
        Log.info("Check is the '%s' check box is selected" % self.name)
        actual_status = super(CheckBox, self).get_attribute(self.attribute)
        if actual_status == self.checked_value:
            return True
        return False


class MultiSelectTree(KOMElement):
    """
        Prefix with mst_
    """

    def __init__(self, ancestor: Ancestor, locator: Locator, select_area: Locator, option_list: Locator,
                 added_item: Locator, delete_item, **kwargs):
        KOMElement.__init__(self, ancestor, locator, **kwargs)
        self._select_area = select_area
        self._option_list = option_list
        self._added_item = added_item
        self._delete_item = delete_item

    def add_item(self, option_name):
        Log.info("Adding %s item to the %s" % (option_name, self.name))
        field = self.get_element()
        field.find_element(self._select_area).click()
        options = field.find_elements(self._option_list)
        for option in options:
            if option.text == option_name:
                option.click()
                break
        field.find_element(self._select_area).click()

    def get_selected_items(self):
        Log.info("Getting all the added items to the %s" % self.name)
        field = self.get_element()
        time.sleep(1)
        items = field.find_elements(self._added_item)
        out = [item.text for item in items]
        return out

    def delete_item(self, item_name):
        Log.info("Deleting %s item to the %s" % (item_name, self.name))
        field = self.get_element()
        time.sleep(1)
        item_index = self.get_selected_items().index(item_name)
        if item_index:
            field.find_element(*self._delete_item).click()


class IFrame(KOMElement):
    """
        Prefix with ifr_
    """

    def switch_to(self):
        Log.info("Switching to iFrame: '%s'" % self.name)
        self.ancestor.switch_to_frame(self.locator)

    def exists(self, wait_time=5, **kwargs) -> bool:
        Log.info("Checking if %s frame exists" % self.name)
        try:
            WebDriverWait(self.get_driver(),
                          wait_time).until(
                expected_conditions.presence_of_element_located(self.locator))
            return True
        except TimeoutException:
            return False


class Image(KOMElement):
    """
        Prefix with img_
    """
    pass


class Spinner(KOMElement):
    """
      Prefix it with spn_
    """

    def wait_for_appear_and_disappear(self, wait_time: int=30):
        Log.info('Wait for %s spinner to appear and disappear' % self.name)
        self.wait_for_visibility(wait_time)
        return self.wait_while_exists(wait_time)


class Form(KOMElement):
    """
      Prefix it with frm_
    """
    pass


class AnyType(KOMElement):
    """
      Prefix it with ant_
    """
    pass
