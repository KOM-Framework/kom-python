import time
from typing import TypeVar, Generic, Callable, List

from kom_framework.src.general import Log
from kom_framework.src.support.locators import Locator
from kom_framework.src.web.datatypes.element_types import Button
from kom_framework.src.web.page_factory import PageFactory
from kom_framework.src.web import element_load_time
from kom_framework.src.web.datatypes.kom_element_list import KOMElementList

T = TypeVar('T')


class Table(Generic[T], KOMElementList):
    """
        Prefix it with tbl_
    """

    def __init__(self, locator: Locator, structure: Callable[[], T],
                 next_page: Locator = None):
        super().__init__(locator)
        self.__structure = structure
        if next_page:
            self.__next_page = Button(next_page)

    def next_page(self):
        if '_Table__next_page' in vars(self).keys():
            if self.__next_page.exists():
                self.__next_page.click()
                return True
        return False

    def get_content(self, wait_time: int = 0) -> List[T]:
        out = []
        if self.exists(wait_time):
            elements = self.wait_for.presence_of_all_elements_located(wait_time)
            for ancestor_index in range(len(elements)):
                structure_object = self.__structure()
                PageFactory.init_elements(structure_object, self, ancestor_index)
                out.append(structure_object)
        return out

    def get_row_by_column_value(self, column_name: str, value: str, wait_time: int = element_load_time) -> T:
        Log.info("Getting row by column %s with value %s from the table: %s" % (column_name, value, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                if getattr(row, column_name).exists():
                    row_value = getattr(row, column_name).text
                    Log.info("Actual text: %s" % row_value)
                    if row_value == value:
                        return row
            if self.next_page():
                return self.get_row_by_column_value(column_name, value, wait_time)
            if time.time() > end_time:
                break
        return None

    def get_row_by_column_text_content(self, column_name: str, value: str, wait_time: int = element_load_time) -> T:
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

    def get_column_values(self, column_name: str, wait_time: int = element_load_time) -> T:
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

    def get_row_by_column_pattern(self, column_name: str, pattern: str, wait_time: int = element_load_time) -> T:
        Log.info("Getting row by column %s with pattern %s from the table: %s" % (column_name, pattern, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                if getattr(row, column_name).exists():
                    row_value = getattr(row, column_name).text
                    if pattern in row_value:
                        return row
            if self.next_page():
                return self.get_row_by_column_pattern(column_name, pattern, wait_time)
            if time.time() > end_time:
                break
        return None

    def get_row_by_index(self, index: int, wait_time: int = element_load_time) -> T:
        Log.info("Getting row by index %s from the table: %s" % (index, self.name))
        rows = self.get_content(wait_time=wait_time)
        return rows[index]

    def get_row_index_by_column_values(self, column_name: str, values: list, wait_time: int = element_load_time) -> T:
        Log.info("Getting row by column %s with value %s from the table: %s" % (column_name, values, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for i in range(len(content)):
                if getattr(content[i], column_name).exists():
                    row_value = getattr(content[i], column_name).text
                    Log.info("Actual text: %s" % row_value)
                    if row_value in values:
                        return i
            if self.next_page():
                return self.get_row_index_by_column_values(column_name, values, wait_time)
            if time.time() > end_time:
                break
        return None

    def get_row_by_attribute_value(self, column_name: str, attribute_name: str, attribute_value: str,
                                   wait_time: int = element_load_time) -> T:
        Log.debug("Getting row by column %s attribute %s and value %s from the table: %s"
                  % (column_name, attribute_name, attribute_value, self.name))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                column = getattr(row, column_name)
                if column.exists():
                    act_attr_value = getattr(row, column_name).get_attribute(attribute_name)
                    if act_attr_value == attribute_value:
                        return row
            if self.next_page():
                return self.get_rows_by_attribute_value(column_name, attribute_name, attribute_value, wait_time)
            elif time.time() > end_time:
                break
        return None

    def get_rows_by_attribute_value(self, column_name: str, attribute_name: str, attribute_value: str,
                                    wait_time: int = element_load_time) -> T:
        Log.debug(f"Getting rows by column {column_name} by attribute {attribute_name} and value {attribute_value} "
                  f"from the table: {self.name}")
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


class Charts(Table[T]):
    """
        Prefix it with chr_
    """
    pass
