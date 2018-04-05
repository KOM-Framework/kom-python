import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ...general import Log
from ...web.data_types.actions import Action
from ...web.data_types.kom_element import KOMElement


class Input(KOMElement):
    """
      Prefix it with inp_
    """

    def __init__(self, locator, message_locator=None, **kwargs):
        KOMElement.__init__(self, locator, **kwargs)
        self.message_locator = message_locator

    def clear(self, use_action_chain=False):
        Log.info("Clearing %s input field" % self._name)
        if use_action_chain:
            ActionChains(self.browser_session.driver).click(self.get_element()) \
                .send_keys(Keys.END) \
                .key_down(Keys.SHIFT) \
                .send_keys(Keys.HOME) \
                .key_up(Keys.SHIFT) \
                .send_keys(Keys.DELETE) \
                .perform()
        else:
            self.execute_action(Action.CLEAR)

    def send_keys(self, value):
        Log.info("Sending %s keys to the '%s' input field" % (value, self._name))
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, str(value))

    def clear_and_send_keys(self, value, use_action_chain=False):
        Log.info("Clearing and sending %s keys to the '%s' input field" % (value, self._name))
        self.clear(use_action_chain)
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, str(value))

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

    def get_message(self):
        if self.message_locator:
            message = AnyType(self.message_locator)
            if message.exists():
                return message.text()
        else:
            raise Exception('Input message locator is not defined')
        return ""


class FRInput(Input):

    def get_content(self):
        return self.execute_action(Action.TEXT)


class TextBlock(KOMElement):
    """
        Prefix it with txt_
    """

    def text(self):
        Log.info("Getting text from the '%s' text block" % self._name)
        return super(TextBlock, self).text()


class TextArea(KOMElement):
    """
        Prefix it with txa_
    """

    def text(self):
        Log.info("Getting text from the '%s' text area" % self._name)
        return super(TextArea, self).text()


class Button(KOMElement):
    """
        Prefix it with btn_
    """

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
    """
        Prefix it with lnk_
    """

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
        if actual_status == 'on':
            actual_status = super(CheckBox, self).get_attribute('checked')
        if (value and actual_status != 'true') or (not value and actual_status == 'true'):
            super(CheckBox, self).click()

    def is_selected(self):
        Log.info("Check is the '%s' check box is selected" % self._name)
        actual_status = super(CheckBox, self).get_attribute('value')
        if actual_status == 'on':
            actual_status = super(CheckBox, self).get_attribute('checked')
        if actual_status == 'true':
            return True
        return False


class MultiSelectTree(KOMElement):

    def __init__(self, locator, select_area, option_list, added_item, delete_item, **kwargs):
        KOMElement.__init__(self, locator, **kwargs)
        self._select_area = select_area
        self._option_list = option_list
        self._added_item = added_item
        self._delete_item = delete_item

    def add_item(self, option_name):
        Log.info("Adding %s item to the %s" % (option_name, self._name))
        field = self.get_element()
        field.find_element(*self._select_area).click()
        options = field.find_elements(*self._option_list)
        for option in options:
            if option.text == option_name:
                option.click()
                break
        field.find_element(*self._select_area).click()

    def get_selected_items(self):
        Log.info("Getting all the added items to the %s" % self._name)
        field = self.get_element()
        time.sleep(1)
        items = field.find_elements(*self._added_item)
        out = [item.text for item in items]
        return out

    def delete_item(self, item_name):
        Log.info("Deleting %s item to the %s" % (item_name, self._name))
        field = self.get_element()
        time.sleep(1)
        item_index = self.get_selected_items().index(item_name)
        if item_index:
            field.find_element(*self._delete_item).click()


class IFrame(KOMElement):

    def switch_to(self):
        Log.info("Switching to iFrame: '%s'" % self._name)
        self.browser_session.switch_to_frame(self.locator)

    def exists(self, wait_time=5, **kwargs):
        Log.info("Checking if %s frame exists" % self._name)
        try:
            WebDriverWait(self.browser_session.driver,
                          wait_time).until(
                expected_conditions.presence_of_element_located(self.locator))
            return True
        except TimeoutException:
            return False


class Image(KOMElement):
    pass


class Spinner(KOMElement):
    """
      Prefix it with spn_
    """
    def wait_for_appear_and_disappear(self, wait_time=30):
        Log.info('Wait for %s spinner to appear and disappear' % self._name)
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
