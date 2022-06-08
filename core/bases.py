"""
Module with metaclasses and abstract metaclasses for various classes
throughout the framework. This module includes a Singleton metaclass
for the logging module, a mixin for the Prototype pattern, Observer and
Subject classes for Observer pattern, BaseSerializer for the framework
"""
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from typing import Any

from jsonpickle import dumps, loads


class NamedSingleton(type):
    """
    Metaclass needed for a realization of a Singleton logging class.
    Checks whether there already exists a logger with a given name
    and then either returns it or creates it (if that is the first time
    such a logger is called upon).
    """

    def __init__(cls, clsname: str, bases: tuple, clsdict: dict, **kwargs):
        """
        Metaclass initialization, creates a private class attribute
        and calls on the __init__() of the super class.

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


class Subject:
    """
    Abstract subject (emitter) class for the Observer pattern.
    """

    def __init__(self):
        """
        Initializes the class object, prepares the list of all
        know observers.
        """
        self.observers = []

    def notify(self):
        """
        Notifies all the observers of the changes.
        """
        for observer in self.observers:
            observer.update(self)


class Observer:
    """
    Abstract observer that updates the data once it receives the
    signal from the Subject. Part of the Observer pattern.
    """

    def update(self, subject: Subject):
        """
        Abstract placeholder-method that does the update.

        :param subject: emitter of the signal
        """
        pass


class User(metaclass=ABCMeta):
    """
    Base metaclass for a user. Main functionality TBD
    """

    def __init__(self, name: str):
        """
        Initializes the class object.

        :param name: username
        """
        self.name = name


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


class BaseSerializer:
    """
    Basic serializer for use in the framework. Utilizes the jsonpickle lib.
    """

    def __init__(self, obj):
        """
        Initializes the serializer object.

        :param obj: object to serialize
        """
        self.object = obj

    def save(self) -> str:
        """
        Serializes the data utilizing the jsonpickle lib.
        """
        return dumps(self.object)

    @staticmethod
    def load(data: Any) -> Any:
        """
        Deserializes the data using the jsonpickle lib.
        """
        return loads(data)


class LoggerStrategy(metaclass=ABCMeta):
    """
    Abstract metaclass for the logger utilizing the Strategy pattern.
    """

    @abstractmethod
    def write(self, text: str):
        """
        Abstract method that must be present in all subclasses of
        the Logger Strategy. Handles the writing of the logs.

        :param text: text to log
        """
        pass
