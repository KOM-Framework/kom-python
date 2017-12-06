class Locator:
    def __init__(self, by, value):
        self.by = by
        self.value = value

    def __call__(self, obj):
        obj._locator = (self.by, self.value)
        return obj
