import time
from typing import TypeVar, Generic, List

from selenium.webdriver import ActionChains

from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.support.web import DriverAware
from ...general import Log
from ...web import element_load_time
from ...web.data_types.kom_element_list import KOMElementList, Structure


class AnyList(KOMElementList):
    """
        Prefix with anl_
    """
    pass


T = TypeVar('T')


class NewTable(Generic[T]):

    def __init__(self,  structure: T, page_object: DriverAware, locator):
        self.structure = structure
        self.__table = KOMElementList(page_object, locator)

    def get_content(self, index=None, wait_time=0) -> List[T]:
        out = []
        # if self.__table.exists(wait_time):
        #     elements = self.__table.wait_for().presence_of_all_elements_located()
        for index in range(2):
            structure_object = self.structure(self.__table, index)
            out.append(structure_object)
        return out


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
        out = []
        if self.exists(wait_time):
            elements = self.wait_for().presence_of_all_elements_located()
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


class Charts(Table):
    """
        Prefix it with chr_
    """
    pass


class Menu(KOMElementList):
    """
        Prefix with mn_
    """

    def select_menu_section_by_name(self, section_name: str) -> bool:
        Log.info("Selecting '%s' section in '%s' menu" % (section_name, self.name))
        sections = self.wait_for().presence_of_all_elements_located()
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
        bar_list = self.wait_for().presence_of_all_elements_located()
        for bar in bar_list:
            ActionChains(bar.parent).move_to_element(bar).perform()
            self.tooltip.exists(element_load_time)
            tooltips = self.tooltip.wait_for().presence_of_all_elements_located()
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
        check_box_list = self.wait_for().presence_of_all_elements_located()
        for check_box in check_box_list:
            if self.is_checked(check_box):
                check_box.click()

    def get_label_value(self, check_box, attribute_name: str='value'):
        label_element = check_box.find_element(*self.label_locator)
        label_attribute_value = label_element.get_attribute(attribute_name)
        return label_attribute_value

    def check_by_attribute_values(self, attribute_name: str, values: list=()):
        check_box_list = self.wait_for().presence_of_all_elements_located()
        for check_box in check_box_list:
            label_attribute_value = self.get_label_value(check_box, attribute_name)
            if label_attribute_value in values:
                check_box.click()

    def get_checked_label_values(self) -> list:
        out = list()
        check_box_list = self.wait_for().presence_of_all_elements_located()
        for check_box in check_box_list:
            if self.is_checked(check_box):
                out.append(self.get_label_value(check_box))
        return out


class RadioGroup(KOMElementList):

    def __init__(self, page_object, group_locator: Locator, label_locator: Locator, **kwargs):
        KOMElementList.__init__(self, page_object, group_locator, **kwargs)
        self.label_locator = label_locator

    def check_by_label_value(self, value):
        check_box_list = self.wait_for().presence_of_all_elements_located()
        for check_box in check_box_list:
            label_element = check_box.find_element(*self.label_locator)
            label_value = label_element.text
            if label_value == value:
                label_element.click()
                break
