from kom_framework.src.web.support.session_factory import WebSessionsFactory


class PageFactory:

    instances = {}

    @classmethod
    def get_instance(cls, key):
        return cls.instances[key]

    @classmethod
    def set_instance(cls, key, page_object):
        cls.instances[key] = page_object


def locator(by, value):
    def real_decorator(class_):
        class WrapperMeta(type):
            def __getattr__(self, attr):
                return getattr(class_, attr)

        class Wrapper(metaclass=WrapperMeta):
            def __new__(cls, *args, **kwargs):
                key = (class_, args, str(kwargs))
                if key not in PageFactory.instances:
                    page_object = class_(*args, **kwargs)
                    page_object._locator = (by, value)
                    WebSessionsFactory.active_frame = None
                    PageFactory.set_instance(key, page_object)
                return PageFactory.get_instance(key)
        return Wrapper
    return real_decorator
