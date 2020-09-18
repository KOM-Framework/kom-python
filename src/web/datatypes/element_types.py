import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select

from .element_list_types import AnyList
from ...general import Log
from ...support.locators import Locator
from ...web.datatypes.actions import Action
from ...web.datatypes.kom_element import KOMElement


class Input(KOMElement):
    """
      Prefix it with inp_
    """

    def __init__(self, locator: Locator, message_locator: Locator = None, **kwargs):
        KOMElement.__init__(self, locator, **kwargs)
        if message_locator:
            self.message = AnyType(message_locator)

    def clear(self):
        Log.info("Clearing %s input field" % self.name)
        self.execute_action(Action.CLEAR)

    def send_keys(self, value: str):
        Log.info("Sending %s keys to the '%s' input field" % (value, self.name))
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, value)

    def clear_and_send_keys(self, value: str):
        Log.info("Clearing and sending %s keys to the '%s' input field" % (value, self.name))
        self.clear()
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, value)

    def type_keys(self, value: str, type_delay: float = 0.1):
        Log.info("Typing %s keys to the '%s' input field" % (value, self.name))
        element = self.wait_for.element_to_be_clickable()
        for ch in value:
            element.send_keys(ch)
            time.sleep(type_delay)

    def get_content(self) -> str:
        return self.execute_action(Action.GET_ATTRIBUTE, presence_of_element_located, "value")

    def get_message(self) -> str:
        if 'message' in dir(self):
            if self.message.exists():
                return self.message.text
            return ''
        else:
            raise Exception('Input message locator is not defined')


class TextBlock(KOMElement):
    """
        Prefix it with txt_
    """


class TextArea(KOMElement):
    """
        Prefix it with txa_
    """


class Button(KOMElement):
    """
        Prefix it with btn_
    """


class PanelItem(KOMElement):
    """
        Prefix with pnl_
    """


class LinkedText(KOMElement):
    """
        Prefix with lkt_
    """


class Link(KOMElement):
    """
        Prefix it with lnk_
    """

    def get_url(self, url_attribute: str = 'href') -> str:
        return self.get_attribute(url_attribute)


class CheckBox(KOMElement):
    """
        Prefix with chk_
    """

    def __init__(self, locator: Locator, attribute: str = 'value', checked_value: str = 'on',
                 **kwargs):
        KOMElement.__init__(self, locator, **kwargs)
        self.attribute = attribute
        self.checked_value = checked_value

    def check(self, value: bool = True):
        Log.info("Checking the '%s' check box" % self.name)
        actual_status = self.get_attribute(self.attribute)
        if (value and actual_status != self.checked_value) or (not value and actual_status == self.checked_value):
            self.click()

    def is_selected(self) -> bool:
        Log.info("Check is the '%s' check box is selected" % self.name)
        actual_status = self.get_attribute(self.attribute)
        if actual_status == self.checked_value:
            return True
        return False


class MultiSelectTree(KOMElement):
    """
        Prefix with mst_
    """

    def __init__(self, locator: Locator, select_area: Locator, option_list: Locator,
                 added_item: Locator, delete_item, **kwargs):
        KOMElement.__init__(self, locator, **kwargs)
        self._select_area = select_area
        self._option_list = option_list
        self._added_item = added_item
        self._delete_item = delete_item

    def add_item(self, option_name):
        Log.info("Adding %s item to the %s" % (option_name, self.name))
        field = self.wait_for.presence_of_element_located()
        field.find_element(self._select_area).click()
        options = field.find_elements(self._option_list)
        for option in options:
            if option.text == option_name:
                option.click()
                break
        field.find_element(self._select_area).click()

    def get_selected_items(self):
        Log.info("Getting all the added items to the %s" % self.name)
        field = self.wait_for.presence_of_element_located()
        time.sleep(1)
        items = field.find_elements(self._added_item)
        out = [item.text for item in items]
        return out

    def delete_item(self, item_name):
        Log.info("Deleting %s item to the %s" % (item_name, self.name))
        field = self.wait_for.presence_of_element_located()
        time.sleep(1)
        item_index = self.get_selected_items().index(item_name)
        if item_index:
            field.find_element(*self._delete_item).click()


class IFrame(KOMElement):
    """
        Prefix with ifr_
    """

    def switch_to(self, wait_time: int = 5):
        Log.info("Switching to iFrame: '%s'" % self.name)
        self.ancestor.switch_to.frame(self.find(wait_time))


class Image(KOMElement):
    """
        Prefix with img_
    """
    pass


class Spinner(KOMElement):
    """
      Prefix it with spn_
    """

    def wait_for_appear_and_disappear(self, wait_time: int = 30):
        Log.info('Wait for %s spinner to appear and disappear' % self.name)
        self.wait_for.visibility_of_element_located(wait_time)
        return self.wait_for.invisibility_of_element_located(wait_time)


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


class SelectExtended(KOMElement):
    """
     Prefix it with slc_
    """

    def __init__(self, link_locator: Locator, option_list_locator: Locator = None,
                 message_locator: Locator = None, extent_list_by_click_on_field: bool = True,
                 hide_list_by_click_on_field: bool = False, **kwargs):
        KOMElement.__init__(self, link_locator, **kwargs)
        self.extent_list_by_click_on_field = extent_list_by_click_on_field
        self.hide_list_by_click_on_field = hide_list_by_click_on_field
        if option_list_locator:
            self.options_list = AnyList(option_list_locator)
        if message_locator:
            self.message = TextBlock(message_locator)

    def get_options(self):
        try:
            return self.options_list.wait_for.presence_of_all_elements_located(0)
        except TimeoutException:
            return []

    def is_expanded(self):
        if self.get_options():
            return True
        return False

    def expand(self, delay_for_options_to_appear_time: int = 0.5):
        if not self.is_expanded():
            self.click()
            time.sleep(delay_for_options_to_appear_time)

    def collapse(self, delay_for_options_to_disappear_time: int = 0.5):
        if self.is_expanded():
            self.click()
            time.sleep(delay_for_options_to_disappear_time)

    def select_item_by_value(self, value: str):
        Log.info('Selecting %s value in the %s select list' % (value, self.name))
        Select(self.find()).select_by_value(value)

    def select_item_by_visible_text(self, value: str):
        Log.info('Selecting %s text in the %s select list' % (value, self.name))
        Select(self.find()).select_by_visible_text(value)

    def first_selected_option(self):
        Log.info('Get first selected option in the %s select list' % self.name)
        return Select(self.find()).first_selected_option.text

    def select_item_by_text(self, text: str, delay_for_options_to_appear_time: int = 0.5):
        Log.info("Selecting %s in the '%s' select list" % (text, self.name))
        if self.extent_list_by_click_on_field:
            self.expand(delay_for_options_to_appear_time)
        options = self.get_options()
        for option in options:
            if option.text == text:
                option.click()
                break
        if self.hide_list_by_click_on_field:
            self.collapse(delay_for_options_to_appear_time)

    def get_options_list(self, delay_for_options_to_appear_time: int = 0.5):
        Log.info("Getting all options list from the '%s' select list" % self.name)
        out = list()
        self.expand(delay_for_options_to_appear_time)
        options = self.get_options()
        for option in options:
            out.append(option.text)
        if self.hide_list_by_click_on_field:
            self.collapse(delay_for_options_to_appear_time)
        return out

    def select_option_by_attribute_value(self, attribute_name: str, attribute_value: str,
                                         delay_for_options_to_appear_time: int = 0.5):
        Log.debug(f"Selecting option by attribute '{attribute_name}' with value '{attribute_value}' "
                  f"in the '{self.name}' select list")
        self.click()
        time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.wait_for.presence_of_all_elements_located()
        for option in options:
            if option.get_attribute(attribute_name) == attribute_value:
                option.click()
                break

    def get_message(self) -> str:
        return self.message.text

    def get_option_attribute_value_by_text(self, option_text: str, attribute_name: str,
                                           delay_for_options_to_appear_time: int = 0.5):
        Log.info(f"Getting options's {option_text} attribute {attribute_name} value in the '%s' select list")
        if self.extent_list_by_click_on_field:
            self.expand(delay_for_options_to_appear_time)
        options = self.get_options()
        for option in options:
            if option.text == option_text:
                actual_value = option.get_attribute(attribute_name)
                return actual_value
        if self.hide_list_by_click_on_field:
            self.collapse(delay_for_options_to_appear_time)
