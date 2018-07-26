from abc import ABCMeta, abstractmethod


class DriverAware:

    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self, **kwargs):
        pass

    @abstractmethod
    def get_driver(self, **kwargs):
        pass
