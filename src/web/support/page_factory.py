def locator(by, value):
    instances = {}

    def real_decorator(class_):
        class Wrapper(class_):
            def __new__(cls, *args, **kwargs):
                key = (class_, args, str(kwargs))
                if key not in instances:
                    page_ob = class_(*args, **kwargs)
                    page_ob._locator = (by, value)
                    instances[key] = page_ob
                return instances[key]
        return Wrapper
    return real_decorator

