from abc import ABCMeta, abstractmethod
from copy import deepcopy


class NamedSingleton(type):
    """
    Metaclass needed for a realization of a Singleton logging class.
    Checks whether there already exists a logger with a given name
    and then either returns it or creates it (if that is the first time
    such a logger is called upon).
    """

    def __init__(cls, clsname, bases, clsdict, **kwargs):
        """
        :param clsname: name of the class
        :param bases: tuple of base classes inherited
        :param clsdict: namespace dictionary of the class
        """
        super().__init__(clsname, bases, clsdict)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs) -> type:
        """
        Main callable method, that checks if instance with a given name
        already exists and either returns this instance or initializes
        a new one.
        """
        name = None
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class PrototypeMixin:
    """
    The mixin for Prototype pattern
    """

    def clone(self):
        """
        The method that utilizes the deepcopy function to create a
        copy of the class-object fed into it.
        :return: a copy of the class-object
        """
        return deepcopy(self)


class User(metaclass=ABCMeta):
    """
    Base metaclass for a user. Main functionality TBD
    """
    pass


class Factory(metaclass=ABCMeta):
    """
    Base metaclass for a factory of anything. Main functionality TBD
    """

    @classmethod
    @abstractmethod
    def create(cls, *args):
        """
        Abstract method used for creation of instances.
        Must be implemented in all factories using this class as meta.
        """
        pass
