import time

from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ...general import Log
from ...web.data_types.actions import Action
from ...web.data_types.kom_element import KOMElement


class Input(KOMElement):
    def send_keys(self, value):
        Log.info("Sending %s keys to the '%s' input field" % (value, self._name))
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, str(value))

    def clear_and_send_keys(self, value, use_action_chain=False):
        Log.info("Clearing and sending %s keys to the '%s' input field" % (value, self._name))
        if use_action_chain:
            ActionChains(self.browser_session.driver).click(self.get_element()) \
                .send_keys(Keys.DELETE) \
                .send_keys(Keys.BACKSPACE) \
                .perform()
            self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, str(value))
        else:
            self.execute_action(Action.CLEAR, expected_conditions.element_to_be_clickable)
            self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, str(value))

    def clear(self):
        Log.info("Clearing %s input field" % self._name)
        self.execute_action(Action.CLEAR)

    def type_keys(self, value):
        Log.info("Typing %s keys to the '%s' input field" % (value, self._name))
        element = self.get_element(expected_conditions.element_to_be_clickable)
        for ch in str(value):
            element.send_keys(ch)
            time.sleep(0.1)

    def send_keys_to_invisible_field(self, value):
        Log.info("Sending %s keys '%s' to the invisible text field" % (value, self._name))
        self.execute_action(Action.SEND_KEYS,  arg=str(value))

    def get_content(self):
        return self.execute_action(Action.GET_ATTRIBUTE, arg="value")


class FRInput(Input):

    def get_content(self):
        return self.execute_action(Action.TEXT)


class TextBlock(KOMElement):
    def text(self):
        Log.info("Getting text from the '%s' text block" % self._name)
        return super(TextBlock, self).text()


class Button(KOMElement):
    def click(self, **kwargs):
        Log.info("Clicking on the '%s' button" % self._name)
        super(Button, self).click(**kwargs)


class PanelItem(KOMElement):
    def click(self, **kwargs):
        Log.info("Clicking on the '%s' panel item" % self._name)
        super(PanelItem, self).click(**kwargs)


class LinkedText(KOMElement):

    def text(self):
        Log.info("Getting text from the '%s' linked text" % self._name)
        return super(LinkedText, self).text()


class Link(KOMElement):

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' web link" % self._name)
        super(Link, self).click(**kwargs)


class CheckBox(KOMElement):

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' check box" % self._name)
        super(CheckBox, self).click(**kwargs)

    def check(self, value=True):
        Log.info("Checking the '%s' check box" % self._name)
        actual_status = super(CheckBox, self).get_attribute('value')
        if (value and actual_status != 'true') or (not value and actual_status == 'true'):
            super(CheckBox, self).click()


class MultiSelectTree(KOMElement):

    def __init__(self, field_by, field_value, select_area, option_list, added_item, delete_item):
        KOMElement.__init__(self, field_by, field_value)
        self._select_area = select_area
        self._option_list = option_list
        self._added_item = added_item
        self._delete_item = delete_item

    def add_item(self, option_name):
        Log.info("Adding %s item to the %s" % (option_name, self._name))
        field = self.get_element()
        field.find_element_by_xpath(self._select_area).click()
        options = field.find_elements_by_xpath(self._option_list)
        for option in options:
            if option.text == option_name:
                option.click()
                break
        field.find_element_by_xpath(self._select_area).click()

    def get_selected_items(self):
        Log.info("Getting all the added items to the %s" % self._name)
        field = self.get_element()
        time.sleep(1)
        items = field.find_elements_by_xpath(self._added_item)
        out = [item.text for item in items]
        return out

    def delete_item(self, item_name):
        Log.info("Deleting %s item to the %s" % (item_name, self._name))
        field = self.get_element()
        time.sleep(1)
        item_index = self.get_selected_items().index(item_name)
        if item_index:
            element = field.find_element_by_xpath('%s[%s]%s' % (self._added_item, str(item_index+1), self._delete_item))
            element.click()


class IFrame(KOMElement):

    def switch_to(self):
        Log.info("Switching to iFrame: '%s'" % self._name)
        self.browser_session.switch_to_frame(self._locator)

    def exists(self, wait_time=5, **kwargs):
        Log.info("Checking if %s frame exists" % self._name)
        try:
            WebDriverWait(self.browser_session.driver,
                          wait_time).until(
                expected_conditions.frame_to_be_available_and_switch_to_it(self._locator))
            self.browser_session.switch_to_default_content()
            return True
        except NoSuchFrameException:
            return False


class Image(KOMElement):
    pass
