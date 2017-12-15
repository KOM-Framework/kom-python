def locator(by, value):
    instances = {}

    def real_decorator(class_):
        def wrapper(*args, **kwargs):
            key = (class_, args, str(kwargs))
            if key not in instances:
                page_ob = class_(*args, **kwargs)
                page_ob._locator = (by, value)
                instances[key] = page_ob
            return instances[key]
        return wrapper
    return real_decorator
