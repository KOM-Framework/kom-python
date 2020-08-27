from kom_framework.src.base_element import KOMElementBase
from kom_framework.src.support.driver_aware import DriverAware


class PageFactory:

    @classmethod
    def init_elements(cls, instance: DriverAware, ancestor: DriverAware, index: int = None):
        elements = vars(instance)
        for element_name in elements:
            element_object = elements[element_name]
            if isinstance(element_object, KOMElementBase):
                cls.init_elements(element_object, ancestor, index)
                element_object.ancestor = ancestor
                if index is not None:
                    element_object.ancestor_index = index


def find_by(locator):
    def real_decorator(class_):
        class WrapperMeta(type):
            def __getattr__(self, attr):
                return getattr(class_, attr)

        class Wrapper(metaclass=WrapperMeta):
            def __new__(cls, *args, **kwargs):
                web_object = class_(*args, **kwargs)
                web_object.locator = locator
                PageFactory.init_elements(web_object, web_object)
                return web_object

        return Wrapper

    return real_decorator
