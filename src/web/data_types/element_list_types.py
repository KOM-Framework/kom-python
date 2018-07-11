import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.support.web import DriverAware
from ...general import Log
from ...web import element_load_time
from ...web.data_types.actions import Action
from ...web.data_types.element_types import Input, TextBlock
from ...web.data_types.kom_element_list import KOMElementList, Structure


class AnyList(KOMElementList):
    """
        Prefix with anl_
    """
    pass


class Table(KOMElementList):
    """
        Prefix it with tbl_
    """

    def __init__(self, page_object: DriverAware, locator: Locator, table_structure: Structure, next_page_button=None,
                 **kwargs):
        KOMElementList.__init__(self, page_object, locator, **kwargs)
        self.table_structure = table_structure
        self.next_page_button = next_page_button

    def next_page(self):
        if self.next_page_button and self.next_page_button.exists():
            self.next_page_button.click()
            return True
        return False

    def get_content(self, index=None, wait_time=0):
        Log.info("Getting content of a table: %s" % self.name)
        end_time = time.time() + wait_time
        out = []
        if self.exists(wait_time):
            elements = []
            while not len(elements):
                elements = self.get_element()
                if time.time() > end_time:
                    break
            out = self.table_structure.init_structure(self, len(elements), index)
        return out

    def get_row_by_column_value(self, column_name, value, wait_time=element_load_time):
        Log.info("Getting row by column %s with value %s from the table: %s" % (column_name, value, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                if getattr(row, column_name).exists():
                    row_value = getattr(row, column_name).text()
                    Log.info("Actual text: %s" % row_value)
                    if row_value == value:
                        return row
            if self.next_page():
                return self.get_row_by_column_value(column_name, value, wait_time)
            if time.time() > end_time:
                break
        return None

    def get_row_by_column_text_content(self, column_name, value, wait_time=element_load_time):
        Log.info("Getting row by column %s with value %s from the table: %s" % (column_name, value, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content(wait_time=wait_time)
            for row in content:
                if getattr(row, column_name).exists():
                    row_value = getattr(row, column_name).get_attribute('textContent')
                    Log.info("Actual text: %s" % row_value)
                    if row_value == value:
                        return row
            if self.next_page():
                return self.get_row_by_column_value(column_name, value, wait_time)
            if time.time() > end_time:
                break
        return None

    def get_column_values(self, column_name, wait_time=element_load_time):
        Log.info("Getting column %s values from the table: %s" % (column_name, self.name))
        column = []
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            if len(content) > 0:
                for row in content:
                    column.append(getattr(row, column_name).get_attribute('textContent'))
                return column
            if time.time() > end_time:
                break
        return None

    def get_row_by_column_pattern(self, column_name, pattern, wait_time=element_load_time):
        Log.info("Getting row by column %s with pattern %s from the table: %s" % (column_name, pattern, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                if getattr(row, column_name).exists():
                    row_value = getattr(row, column_name).text()
                    if pattern in row_value:
                        return row
            if self.next_page():
                return self.get_row_by_column_pattern(column_name, pattern, wait_time)
            if time.time() > end_time:
                break
        return None

    def get_row_by_index(self, index, wait_time=element_load_time):
        Log.info("Getting row by index %s from the table: %s" % (index, self.name))
        element = self.get_content(index, wait_time=wait_time)
        return element

    def get_rows_by_attribute_value(self, column_name, attribute_name, attribute_value, wait_time=element_load_time):
        Log.info("Getting rows by column %s by attribute %s and value %s from the table: %s"
                 % (column_name, attribute_name, attribute_value, self.name))
        out = list()
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                column = getattr(row, column_name)
                if column.exists():
                    act_attr_value = getattr(row, column_name).get_attribute(attribute_name)
                    if act_attr_value == attribute_value:
                        out.append(row)
            if self.next_page():
                return self.get_rows_by_attribute_value(column_name, attribute_name, attribute_value, wait_time)
            elif out or time.time() > end_time:
                break
        return out


class WebGroup(Table):
    """
        Prefix with wbg_
    """

    def select_by_text(self, text):
        Log.info("Selecting %s text in the %s group" % (text, self.name))
        elements = self.get_element()
        for element in elements:
            if element.text == text:
                element.click()
                break


class Charts(Table):
    """
        Prefix it with chr_
    """
    pass


class SelectList(KOMElementList):
    """
     Prefix it with slc_
    """

    def __init__(self, page_object: DriverAware, link_locator: Locator, option_list_locator: Locator=None,
                 message_locator: Locator=None, extent_list_by_click_on_field: bool=True,
                 hide_list_by_click_on_field: bool=False, **kwargs):
        KOMElementList.__init__(self, page_object, link_locator, **kwargs)
        self.extent_list_by_click_on_field = extent_list_by_click_on_field
        self.hide_list_by_click_on_field = hide_list_by_click_on_field
        if option_list_locator:
            self.options_list = KOMElementList(page_object, option_list_locator)
        if message_locator:
            self.message = TextBlock(page_object, message_locator)

    def select_item_by_value(self, value: str):
        Log.info('Selecting %s value in the %s select list' % (value, self.name))
        Select(self.get_element()).select_by_value(value)

    def select_item_by_visible_text(self, value: str):
        Log.info('Selecting %s text in the %s select list' % (value, self.name))
        Select(self.get_element()).select_by_visible_text(value)

    def first_selected_option(self):
        Log.info('Get first selected option in the %s select list' % self.name)
        return Select(self.get_element()).first_selected_option

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' select list" % self.name)
        super(SelectList, self).click(**kwargs)

    def select_item_by_text(self, text: str, delay_for_options_to_appear_time: int=0.5):
        Log.info("Selecting %s in the '%s' select list" % (text, self.name))
        if self.extent_list_by_click_on_field:
            self.execute_action(Action.CLICK)
            time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.get_element()
        for option in options:
            if option.text == text:
                option.click()
                break
        if self.hide_list_by_click_on_field:
            self.execute_action(Action.CLICK)

    def get_options_list(self, delay_for_options_to_appear_time: int=0.5):
        Log.info("Getting all options list from the '%s' select list" % self.name)
        out = list()
        self.execute_action(Action.CLICK)
        time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.get_element()
        for option in options:
            out.append(option.text)
        return out

    def select_option_by_attribute_value(self, attribute_name: str, attribute_value: str,
                                         delay_for_options_to_appear_time: int=0.5):
        Log.info("Selecting option by attribute '%s' with value '%s' in the '%s' select list"
                 % (attribute_name, attribute_value, self.name))
        self.execute_action(Action.CLICK)
        time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.get_element()
        for option in options:
            if option.get_attribute(attribute_name) == attribute_value:
                option.click()
                break

    def get_message(self) -> str:
        return self.message.text()


class SelectMenu(KOMElementList):
    """
        Prefix with slm_
    """

    def __init__(self, ancestor: DriverAware, locator: Locator, list_locator: Locator=None, **kwargs):
        KOMElementList.__init__(self, ancestor, locator, **kwargs)
        self.list_locator = list_locator

    def select_item_by_text(self, text: str):
        Log.info("Selecting %s in the '%s' select menu" % (text, self.name))
        text_field = Input(self.ancestor, self.locator)
        text_field.clear()
        text_field.type_keys(text)
        time.sleep(0.5)
        options = KOMElementList(self.ancestor, self.list_locator).get_element()
        for option in options:
            if text in option.get_attribute('title'):
                option.click()
                break


class Menu(KOMElementList):
    """
        Prefix with mn_
    """

    def select_menu_section_by_name(self, section_name: str) -> bool:
        Log.info("Selecting '%s' section in '%s' menu" % (section_name, self.name))
        sections = self.get_element()
        for section in sections:
            if section.text == section_name:
                section.click()
                Log.info("Selected '%s' section in '%s' menu" % (section_name, self.name))
                return True
        Log.info("Selecting '%s' section in '%s' menu failed" % (section_name, self.name))
        return False


class BarChart(KOMElementList):
    """
        Prefix with mn_
    """
    def __init__(self, page_object: DriverAware, locator: Locator, tooltip_locator: Locator=None, **kwargs):
        KOMElementList.__init__(self, page_object, locator, **kwargs)
        if tooltip_locator:
            self.tooltip = KOMElementList(page_object, tooltip_locator)

    def get_tooltip_lines_text(self) -> list:
        out = list()
        bar_list = self.get_element()
        for bar in bar_list:
            ActionChains(bar.parent).move_to_element(bar).perform()
            time.sleep(0.5)
            tooltips = self.tooltip.get_element()
            data = list()
            for line in tooltips:
                data.append(line.text)
            out.append(data)
        return out


class CheckBoxList(KOMElementList):

    def __init__(self, page_object, locator: Locator, label_locator: Locator, **kwargs):
        KOMElementList.__init__(self, page_object, locator, **kwargs)
        self.label_locator = label_locator

    @staticmethod
    def is_checked(check_box):
        return 'checked' in check_box.get_attribute('class')

    def uncheck_all(self):
        check_box_list = self.get_element()
        for check_box in check_box_list:
            if self.is_checked(check_box):
                check_box.click()

    def get_label_value(self, check_box, attribute_name: str='value'):
        label_element = check_box.find_element(*self.label_locator)
        label_attribute_value = label_element.get_attribute(attribute_name)
        return label_attribute_value

    def check_by_attribute_values(self, attribute_name: str, values: list=()):
        check_box_list = self.get_element()
        for check_box in check_box_list:
            label_attribute_value = self.get_label_value(check_box, attribute_name)
            if label_attribute_value in values:
                check_box.click()

    def get_checked_label_values(self) -> list:
        out = list()
        check_box_list = self.get_element()
        for check_box in check_box_list:
            if self.is_checked(check_box):
                out.append(self.get_label_value(check_box))
        return out


class RadioGroup(KOMElementList):

    def __init__(self, page_object, group_locator: Locator, label_locator: Locator, **kwargs):
        KOMElementList.__init__(self, page_object, group_locator, **kwargs)
        self.label_locator = label_locator

    def check_by_label_value(self, value):
        check_box_list = self.get_element()
        for check_box in check_box_list:
            label_element = check_box.find_element(*self.label_locator)
            label_value = label_element.text
            if label_value == value:
                label_element.click()
                break
