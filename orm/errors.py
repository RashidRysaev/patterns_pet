"""
Module containing custom errors for use with the framework's ORM.
"""
from typing import Tuple, Any


class RecordNotFoundError(Exception):
    """
    Exception raised when there's no such record in the DB.
    """

    def __init__(self, message: str):
        """
        Initializes the error with the custom error message.

        :param message:
        """
        super().__init__(f'Record not found in database: {message}')


class DatabaseCommitError(Exception):
    """
    Exception raised when there's a problem committing changes to the DB.
    """

    def __init__(self, message: Tuple[Any, ...]):
        """
        Initializes the error with the custom error message.

        :param message:
        """
        super().__init__(f'Error committing changes to database: {message}')


class DatabaseUpdateError(Exception):
    """
    Exception raised when there's a problem updating the DB.
    """

    def __init__(self, message: Tuple[Any, ...]):
        """
        Initializes the error with the custom error message.

        :param message:
        """
        super().__init__(f'Error updating database: {message}')


class DatabaseDeleteError(Exception):
    """
    Exception raised when there's a problem deleting from the DB.
    """

    def __init__(self, message: Tuple[Any, ...]):
        """
        Initializes the error with the custom error message.

        :param message:
        """
        super().__init__(f'Error deleting from database: {message}')
