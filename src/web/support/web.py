from abc import ABCMeta, abstractmethod


class DriverAware:

    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self, **kwargs):
        raise NotImplementedError

    @property
    def driver(self):
        raise NotImplementedError
