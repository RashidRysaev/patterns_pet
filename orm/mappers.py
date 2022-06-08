from sqlite3 import connect, Connection

from models import Student
from orm.errors import RecordNotFoundError, DatabaseCommitError, \
    DatabaseUpdateError, DatabaseDeleteError

connection = connect('test_db.sqlite3')


class StudentMapper:
    def __init__(self, conn: Connection):
        self.connection = conn
        self.cursor = conn.cursor()
        self.table_name = 'students'

    def return_all(self) -> list:
        statement = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            item_id, item_name = item
            student = Student(item_name)
            student.id = item_id
            result.append(student)
        return result

    def find_by_id(self, id: int):
        statement = f'SELECT id, name FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundError(f'Record with id={id} not found!')

    def insert(self, obj):
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseCommitError(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.table_name} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseUpdateError(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseDeleteError(e.args)


# TODO mapper metaclass or parent class? and separate mappers for
#  all types of objects in the framework

# TODO docstrings and such...

class MapperRegistry:
    mappers = {
        'student': StudentMapper
    }

    @staticmethod
    def get_mapper(obj: object):
        if isinstance(obj, StudentMapper):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name: str):
        return MapperRegistry.mappers[name](connection)
