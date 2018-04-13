import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from ...general import Log
from ...web import element_load_time
from ...web.data_types.actions import Action
from ...web.data_types.element_types import Input, AnyType
from ...web.data_types.kom_element_list import KOMElementList


class AnyList(KOMElementList):
    """
        Prefix with anl_
    """
    pass


class Table(KOMElementList):
    """
        Prefix it with tbl_
    """

    def __init__(self, locator, table_structure, next_page_button=None, **kwargs):
        KOMElementList.__init__(self, locator, **kwargs)
        self.table_structure = table_structure
        self.next_page_button = next_page_button

    def next_page(self):
        if self.next_page_button and self.next_page_button.exists():
            self.next_page_button.click()
            return True
        return False

    def get_content(self, specific_index=None, wait_time=0):
        Log.info("Getting content of a table: %s" % self._name)
        end_time = time.time() + wait_time
        out = []
        if self.exists(wait_time):
            elements = []
            while not len(elements):
                elements = self.get_elements()
                if time.time() > end_time:
                    break
            elements_count = len(elements)
            field_names = self.table_structure.keys()
            for i in range(elements_count):
                if specific_index is not None:
                    i = specific_index
                obj = self.table_structure.get_copy()
                for field in field_names:
                    field_object = getattr(obj, field)
                    setattr(field_object, '_ancestor_element', self)
                    setattr(field_object, '_base_element_index', i)
                if specific_index is not None:
                    obj.test = elements[specific_index]
                    return obj
                out.append(obj)
        return out

    def get_row_by_column_value(self, column_name, value, wait_time=element_load_time):
        Log.info("Getting row by column %s with value %s from the table: %s" % (column_name, value, self._name))
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

    def get_column_values(self, column_name, wait_time=element_load_time):
        Log.info("Getting column %s values from the table: %s" % (column_name, self._name))
        column = []
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            if len(content) > 0:
                for row in content:
                    column.append(getattr(row, column_name).text())
                return column
            if time.time() > end_time:
                break
        return None

    def get_row_by_column_pattern(self, column_name, pattern, wait_time=element_load_time):
        Log.info("Getting row by column %s with pattern %s from the table: %s" % (column_name, pattern, self._name))
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
        Log.info("Getting row by index %s from the table: %s" % (index, self._name))
        element = self.get_content(index, wait_time=wait_time)
        return element

    def wait_for_visibility(self, wait_time=element_load_time):
        Log.info('Waiting for the grid %s to be visible' % self._name)
        WebDriverWait(self.browser_session.driver, wait_time).until(
            expected_conditions.presence_of_all_elements_located(self.locator)
        )

    def wait_for_elements_count(self, elements_count, wait_time):
        Log.info('Waiting for the %s elements appears in a grid %s' % (elements_count, self._name))
        try:
            WebDriverWait(self.browser_session.driver, wait_time).until(
                lambda driver: len(driver.find_elements(*self.locator)) == elements_count)
            return True
        except TimeoutException:
            return False

    def get_rows_by_attribute_value(self, column_name, attribute_name, attribute_value, wait_time=element_load_time):
        Log.info("Getting rows by column %s by attribute %s and value %s from the table: %s"
                 % (column_name, attribute_name, attribute_value, self._name))
        out = list()
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                if getattr(row, column_name).exists():
                    act_attr_value = getattr(row, column_name).get_attribute(attribute_name)
                    if act_attr_value == attribute_value:
                        out.append(row)
            if self.next_page():
                return self.get_rows_by_attribute_value(column_name, attribute_name, attribute_value, wait_time)
            if time.time() > end_time:
                break
        return out


class WebGroup(Table):

    def select_by_text(self, text):
        Log.info("Selecting %s text in the %s group" % (text, self._name))
        elements = self.get_elements()
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

    def __init__(self, link_locator, option_list_locator=None, message_locator=None,
                 extent_list_by_click_on_field=True, hide_list_by_click_on_field=False,
                 **kwargs):
        KOMElementList.__init__(self, link_locator, **kwargs)
        self.extent_list_by_click_on_field = extent_list_by_click_on_field
        self.hide_list_by_click_on_field = hide_list_by_click_on_field
        if option_list_locator:
            self.options_list = KOMElementList(option_list_locator)
        if message_locator:
            self.message = AnyType(message_locator)

    def select_item_by_value(self, value):
        Log.info('Selecting %s value in the %s select list' % (value, self._name))
        Select(self.get_element()).select_by_value(value)

    def select_item_by_visible_text(self, value):
        Log.info('Selecting %s text in the %s select list' % (value, self._name))
        Select(self.get_element()).select_by_visible_text(value)

    def first_selected_option(self):
        Log.info('Get first selected option in the %s select list' % self._name)
        return Select(self.get_element()).first_selected_option

    def click(self, **kwargs):
        Log.info("Clicking on the '%s' select list" % self._name)
        super(SelectList, self).click(**kwargs)

    def select_item_by_text(self, text):
        Log.info("Selecting %s in the '%s' select list" % (text, self._name))
        if self.extent_list_by_click_on_field:
            self.execute_action(Action.CLICK)
        options = self.options_list.get_elements()
        for option in options:
            if option.text == text:
                option.click()
                break
        if self.hide_list_by_click_on_field:
            self.execute_action(Action.CLICK)

    def get_options_list(self):
        Log.info("Getting all options list from the '%s' select list" % self._name)
        out = list()
        self.execute_action(Action.CLICK)
        options = self.options_list.get_elements()
        for option in options:
            out.append(option.text)
        return out

    def select_option_by_attribute_value(self, attribute_name, attribute_value):
        Log.info("Selecting option by attribute '%s' with value '%s' in the '%s' select list"
                 % (attribute_name, attribute_value, self._name))
        self.execute_action(Action.CLICK)
        options = self.options_list.get_elements()
        for option in options:
            if option.get_attribute(attribute_name) == attribute_value:
                option.click()
                break

    def get_message(self):
        return self.message.text()


class SelectMenu(KOMElementList):

    def __init__(self, locator, list_locator=None, **kwargs):
        KOMElementList.__init__(self, locator, **kwargs)
        self.list_locator = list_locator

    def select_item_by_text(self, text):
        Log.info("Selecting %s in the '%s' select menu" % (text, self._name))
        text_field = Input(self.locator)
        text_field.clear()
        text_field.type_keys(text)
        time.sleep(0.5)
        options = KOMElementList(self.list_locator).get_elements()
        for option in options:
            if text in option.get_attribute('title'):
                option.click()
                break


class Menu(KOMElementList):

    def select_menu_section_by_name(self, section_name):
        Log.info("Selecting '%s' section in '%s' menu" % (section_name, self._name))
        sections = self.get_elements()
        for section in sections:
            if section.text == section_name:
                section.click()
                Log.info("Selected '%s' section in '%s' menu" % (section_name, self._name))
                return True
        Log.info("Selecting '%s' section in '%s' menu failed" % (section_name, self._name))
        return False


class BarChart(KOMElementList):
    def __init__(self, locator, tooltip_locator=None, **kwargs):
        KOMElementList.__init__(self, locator, **kwargs)
        if tooltip_locator:
            self.tooltip = KOMElementList(tooltip_locator)

    def get_tooltip_lines_text(self):
        out = list()
        bar_list = self.get_elements()
        for bar in bar_list:
            ActionChains(self.browser_session.driver).move_to_element(bar).perform()
            time.sleep(0.5)
            tooltips = self.tooltip.get_elements()
            data = list()
            for line in tooltips:
                data.append(line.text)
            out.append(data)
        return out
