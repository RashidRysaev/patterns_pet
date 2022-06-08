"""
This module contains realizations for two basic classes required
for an ORM - UnitOfWork (based on the patter of the same name) and
DomainObject, which is an abstract parent class for any object
that should be able to be committed to the database.
"""
from threading import local


class UnitOfWork:
    """
    A realization of the Unit Of Work pattern - common pattern
    used to work with databases. It keeps track of the changes
    to the objects and doesn't allow for multiple simultaneous
    changes of the same object.
    """
    current = local()

    def __init__(self):
        """
        Initializes the session class. Creates the lists with
        new, modified and deleted objects.
        """
        self.mapper_registry = None
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, registry):
        """
        Sets the data mapper registry.

        :param registry: the registry with all available mappers
        """
        self.mapper_registry = registry

    def register_new(self, obj: object):
        """
        First it clears the list with new objects in case
        there are any left from previous iterations, then
        adds a new object to the session.

        :param obj: any object
        """
        self.new_objects.clear()
        self.new_objects.append(obj)

    def register_dirty(self, obj: object):
        """
        First it clears the list with modified objects in case
        there are any left from previous iterations, then
        adds a modified object to the session.

        :param obj: any object
        """
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        """
        First it clears the list with objects for deletion in case
        there are any left from previous iterations, then
        adds an object for deletion to the session.

        :param obj: any object
        """
        self.removed_objects.append(obj)

    def commit(self):
        """
        Commits the changes to the database by consecutively triggering
        three different methods that first insert new entries to the
        database, then update the existing entries, and then delete
        the existing entries from the database.
        """
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        """
        Inserts new entries to the database. Uses a for-loop
        on the list and inserts each object one by one using
        the object's mapper.
        """
        for obj in self.new_objects:
            self.mapper_registry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        """
        Updates the entries in the database. Uses a for-loop
        on the list and updates each object one by one using
        the object's mapper.
        """
        for obj in self.dirty_objects:
            self.mapper_registry.get_mapper(obj).update(obj)

    def delete_removed(self):
        """
        Deletes the entries from the database. Uses a for-loop
        on the list and deletes each object one by one using
        the object's mapper.
        """
        for obj in self.removed_objects:
            self.mapper_registry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        """
        Static method that triggers the setting of the new
        current thread.
        """
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        """
        Main method that sets the new local thread.

        :param unit_of_work: an instance of the class
        """
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        """
        Returns the current local thread.

        :return: current instance of the class
        """
        return cls.current.unit_of_work


class DomainObject:
    """
    Abstract parent class for an abstract object to be used
    in the ORM.
    """

    def mark_new(self):
        """
        Marks the current object as a new one.
        """
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        """
        Marks the current object as a modified one.
        """
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        """
        Marks the current object for deletion.
        """
        UnitOfWork.get_current().register_removed(self)
