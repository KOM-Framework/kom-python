from selenium.webdriver import ActionChains

from ...general import Log
from ...support.locators import Locator
from ...web import element_load_time
from ...web.datatypes.kom_element_list import KOMElementList


class AnyList(KOMElementList):
    """
        Prefix with anl_
    """
    pass


class Menu(KOMElementList):
    """
        Prefix with mn_
    """

    def select_menu_section_by_name(self, section_name: str) -> bool:
        Log.info("Selecting '%s' section in '%s' menu" % (section_name, self.name))
        sections = self.wait_for.presence_of_all_elements_located()
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

    def __init__(self, locator: Locator, tooltip_locator: Locator = None, **kwargs):
        KOMElementList.__init__(self, locator, **kwargs)
        if tooltip_locator:
            self.tooltip = KOMElementList(tooltip_locator)

    def get_tooltip_lines_text(self) -> list:
        out = list()
        bar_list = self.wait_for.presence_of_all_elements_located()
        for bar in bar_list:
            ActionChains(bar.parent).move_to_element(bar).perform()
            self.tooltip.exists(element_load_time)
            tooltips = self.tooltip.wait_for.presence_of_all_elements_located()
            data = list()
            for line in tooltips:
                data.append(line.text)
            out.append(data)
        return out


class CheckBoxList(KOMElementList):

    def __init__(self, locator: Locator, label_locator: Locator, **kwargs):
        KOMElementList.__init__(self, locator, **kwargs)
        self.label_locator = label_locator

    @staticmethod
    def is_checked(check_box):
        return 'checked' in check_box.get_attribute('class')

    def uncheck_all(self):
        check_box_list = self.wait_for.presence_of_all_elements_located()
        for check_box in check_box_list:
            if self.is_checked(check_box):
                check_box.click()

    def get_label_value(self, check_box, attribute_name: str = 'value'):
        label_element = check_box.find_element(*self.label_locator)
        label_attribute_value = label_element.get_attribute(attribute_name)
        return label_attribute_value

    def check_by_attribute_values(self, attribute_name: str, values: list = ()):
        check_box_list = self.wait_for.presence_of_all_elements_located()
        for check_box in check_box_list:
            label_attribute_value = self.get_label_value(check_box, attribute_name)
            if label_attribute_value in values:
                check_box.click()

    def get_checked_label_values(self) -> list:
        out = list()
        check_box_list = self.wait_for.presence_of_all_elements_located()
        for check_box in check_box_list:
            if self.is_checked(check_box):
                out.append(self.get_label_value(check_box))
        return out


class RadioGroup(KOMElementList):
    """
        Prefix with rdg_
    """

    def __init__(self, group_locator: Locator, label_locator: Locator, **kwargs):
        KOMElementList.__init__(self, group_locator, **kwargs)
        self.label_locator = label_locator

    def check_by_label_value(self, value):
        check_box_list = self.wait_for.presence_of_all_elements_located()
        for check_box in check_box_list:
            label_element = check_box.find_element(*self.label_locator)
            label_value = label_element.text
            if label_value == value:
                label_element.click()
                break
