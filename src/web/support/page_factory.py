from kom_framework.src.general import get_obj_key


class PageFactory:

    instances = {}

    @classmethod
    def get_instance(cls, key):
        return cls.instances[key]

    @classmethod
    def set_instance(cls, key, page_object):
        cls.instances[key] = page_object


def find_by(locator):
    def real_decorator(class_):
        class WrapperMeta(type):
            def __getattr__(self, attr):
                return getattr(class_, attr)

        class Wrapper(metaclass=WrapperMeta):
            def __new__(cls, *args, **kwargs):
                key = get_obj_key(class_, args, kwargs)
                if key not in PageFactory.instances:
                    page_object = cls.create_object(*args, **kwargs)
                    PageFactory.set_instance(key, page_object)
                    return PageFactory.get_instance(key)
                else:
                    return cls.create_object(*args, **kwargs)

            @staticmethod
            def create_object(*args, **kwargs):
                page_object = class_(*args, **kwargs)
                page_object.locator = locator
                return page_object
        return Wrapper
    return real_decorator
