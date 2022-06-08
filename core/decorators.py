"""
Module that contains decorators used throughout the framework. Namely,
it contains the class-based decorator for URL routes and the debugging
decorator that measures the performance time of the method or function
it is used on.
"""
from time import perf_counter
from typing import Callable

from core.bases import NamedSingleton


class UrlPaths(metaclass=NamedSingleton):
    """
    The URL Paths class. All the paths are stored in the class' attribute -
    URL dictionary. The path itself serves as key to the dictionary, and the
    link to the CBV-object in the memory serves as the value. The metaclass
    here is NamedSingleton to ensure that the object returned does indeed
    have the URLs added into it earlier. The class uses a decorator function
    add_route to gather the URL routes.
    """
    URLS = {}

    def __init__(self, name='urlpaths'):
        """
        Initializes the instance. The 'name' parameter is the legacy
        of the NamedSingleton metaclass, but it's been given a name
        by default, since there can only be one!

        :param name: name of the object
        """
        self.name = name

    def add_route(self, url: str) -> Callable:
        """
        Decorates the callable view class to update the list of url-paths
        in the framework. The url-string becomes the key in the
        url-paths dictionary.

        :param url: a string with the url-address
        """

        def wrapped(view: Callable, *args, **kwargs):
            """
            Decorated callable function passed by the decorator method.
            It becomes the value of the url-paths dictionary

            :param view: class-based view
            """
            self.URLS[url] = view(*args, **kwargs)

        return wrapped


def debug(func: Callable) -> Callable:
    """
    Decorates the function in order to measure its runtime. If you use
    it on a class' method, unfortunately for now it can only give you the
    name of the method, but not the name of the class which this method
    belongs to.

    :param func: callable function or method
    """
    def wrapped(*args, **kwargs):
        """
        Decorated callable function. Can be anything really, not just views.
        """
        start = perf_counter()
        res = func(*args, **kwargs)
        finish = perf_counter()
        print(f'DEBUG.\n'
              f'Function: {func.__name__};\n'
              f'Function run time: {finish - start} sec.')
        return res

    return wrapped
