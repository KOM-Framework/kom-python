from kom_framework.src.base_element import KOMElementBase
from kom_framework.src.support.locators import Xpath
from kom_framework.src.support.driver_aware import DriverAware


class WindowFactory:

    @classmethod
    def init_elements(cls, instance: DriverAware, ancestor: DriverAware):
        elements = vars(instance)
        for element_name in elements:
            element_object = elements[element_name]
            if isinstance(element_object, KOMElementBase):
                element_object.ancestor = ancestor


def find_by(locator: Xpath):
    def real_decorator(class_):
        class WrapperMeta(type):
            def __getattr__(self, attr):
                return getattr(class_, attr)

        class Wrapper(metaclass=WrapperMeta):
            def __new__(cls, *args, **kwargs):
                win_object = class_(*args, **kwargs)
                win_object.locator = locator
                WindowFactory.init_elements(win_object, win_object)
                return win_object

        return Wrapper

    return real_decorator
