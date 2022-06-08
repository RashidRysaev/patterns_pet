"""
Module containing models for future use with the ORM and classes
(e.g. factories) used by the main OnlineUniversity class.
"""
from core.bases import User, Factory, PrototypeMixin, Subject, Observer
from orm.core import DomainObject


class CourseCategory:
    """
    Class representing the categories of the courses in the ORM.
    """
    auto_id = 0

    def __init__(self, name: str, category):
        """
        Initializes the course category, increases the auto_id by 1.

        :param name: category name
        :param category: can be either a CourseCategory object or None
        """
        self.id = CourseCategory.auto_id
        CourseCategory.auto_id += 1
        self.name = name
        self.category = category
        self.existing_courses = []

    def count_courses(self) -> int:
        """
        Counts the number of existing courses and returns the value.

        :return: the number of existing courses.
        """
        res = len(self.existing_courses)
        if self.category:
            res += self.category.count_courses()
        return res


class Course(PrototypeMixin, Subject):
    """
    Main abstract class for courses, inherits from the Prototype Mixin
    which allows for cloning of existing courses.
    """

    def __init__(self, course_name: str, course_category: CourseCategory):
        """
        Initializes the Course object and appends it to the list of
        existing courses.

        :param course_name:
        :param course_category:
        """
        self.name = course_name
        self.category = course_category
        self.category.existing_courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        """
        Redefines the built-in magic method - allows for the following
        call: Course[Student], which would return a student enlisted
        in the course.

        :param item: student in question
        :return: a Student object
        """
        return self.students[item]

    def add_student(self, student):
        """
        Handles the addition of a new student to the course on the course's
        side.

        :param student:
        """
        self.students.append(student)
        student.courses_in_attendance.append(self)
        self.notify()


class OnlineCourse(Course):
    """
    Class representing the online (pre-recorded) courses in the ORM.
    """

    def __init__(self, course_name: str, course_category: CourseCategory):
        """
        Initializes the online course. Sets the number of pre-recorded
        lessons to 0.

        :param course_name:
        :param course_category:
        """
        super().__init__(course_name, course_category)
        self.number_of_lessons = 0


class OfflineCourse(Course):
    """
    Class representing the offline courses in the ORM.
    """

    def __init__(self, course_name: str, course_category: CourseCategory):
        """
        Initializes the offline course. Creates the address attribute to
        be filled later.

        :param course_name:
        :param course_category:
        """
        super().__init__(course_name, course_category)
        self.address = None


class WebinarCourse(Course):
    """
    Class representing the webinars in the ORM.
    """

    def __init__(self, course_name: str, course_category: CourseCategory):
        """
        Initializes the webinar course.

        :param course_name:
        :param course_category:
        """
        super().__init__(course_name, course_category)


class CourseFactory(Factory):
    """
    Factory class used for creation of the courses.
    course_types is a dictionary that stores information about all
    available course types.
    """
    course_types = {
        'online': OnlineCourse,
        'offline': OfflineCourse,
        'webinar': WebinarCourse
    }

    @classmethod
    def create(
            cls, type_: str, name: str, category: CourseCategory) -> Course:
        """
        Creates the course of the given type with the given name under
        the given category.

        :param type_: type of the course
        :param name: name of the course
        :param category: course category
        :return: an instance of the given Course subclass
        """
        return cls.course_types[type_](name, category)


class Teacher(User):
    """
    Class representing teachers in the ORM.
    """


class Student(User, DomainObject):
    """
    Class representing students in the ORM.
    """

    def __init__(self, name: str):
        """
        Initializes the instance of Student class and creates
        the list with courses this student is attending

        :param name: student's login
        """
        super().__init__(name)
        self.id = None
        self.courses_in_attendance = []

    def attend_course(self, course: Course):
        """
        Enlists the student on a course. First checks if this student
        already attends the course, if not - enlists, otherwise - prints
        an error message.

        :param course: the course to be enlisted on
        """
        already_attending_flag = self.courses_in_attendance.count(course)
        if not already_attending_flag:
            self.courses_in_attendance.append(course)
        else:
            print('You are already attending this course.')

    def leave_course(self, course: Course):
        """
        Removes the student from the course if he doesn't wish to attend it.
        For now it's as simple as this.

        :param course: the course the student wishes to leave
        """
        try:
            self.courses_in_attendance.remove(course)
        except ValueError:
            print('You are not attending this course!')


class UserFactory(Factory):
    """
    Factory class used for creation of the users.
    user_types is a dictionary that stores information about
    all available user types.
    """
    user_types = {
        'teacher': Teacher,
        'student': Student
    }

    @classmethod
    def create(cls, type_: str, name: str) -> User:
        """
        Creates the users of the given type.

        :param type_: the type of the user in string format
        :param name: username
        :return: a new instance of the given class
        """
        return cls.user_types[type_](name)


class TextMessageNotifier(Observer):
    """
    Class that observes the changes to the courses, e.g. when a new student
    enlists in a course, and sends text messages regarding that. Not really
    sends though, it's a spoof.
    """

    def update(self, subject: Course):
        """
        Sends text messages once the signal from the Subject-subclass
        object is emitted.

        :param subject: course that emitted the signal
        """
        print(f'Text message sent!'
              f'"Student {subject.students[-1]} joined {subject.name} course"')


class EmailNotifier(Observer):
    """
    Class that observes the changes to the courses, e.g. when a new student
    enlists in a course, and sends emails regarding that. Not really sends
    though, it's a spoof.
    """

    def update(self, subject: Course):
        """
        Sends emails once the signal from the Subject-subclass object
        is emitted.

        :param subject: course that emitted the signal
        """
        print(f'Email sent!'
              f'"Student {subject.students[-1]} joined {subject.name} course"')


class OnlineUniversity:
    """
    The main class of the online university, built with this simple
    WSGI framework.
    """

    def __init__(self):
        """
        Initializes the main class.
        Creates the necessary data structures.
        """
        self.teachers = []
        self.students = []
        self.course_categories = []
        self.courses = []

    @staticmethod
    def create_user(type_: str, name: str) -> User:
        """
        Creates the user with the help of the user factory.

        :param type_: string with the user type
        :param name: username
        :return: an instance of one of the User subclasses
        """
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(
            name: str, category: CourseCategory = None) -> CourseCategory:
        """
        Creates a course category with the given name. Can also
        take the already existing category, but that is not mandatory.

        :param name: category name
        :param category: existing category
        :return: an instance of the CourseCategory class
        """
        return CourseCategory(name, category)

    def find_category(self, cat_id: int) -> CourseCategory:
        """
        Looks for an existing category by its ID.
        If nothing found raises an exception.

        :param cat_id: category ID
        :return: an instance of CourseCategory class
        """
        for item in self.course_categories:
            if item.id == cat_id:
                return item
        raise Exception(f"There's no category with id {cat_id}")

    @staticmethod
    def create_course(
            type_: str, name: str, category: CourseCategory) -> Course:
        """
        Creates a course of the given type, with the given name and
        under the given category.

        :param type_: the type of the course
        :param name: the name of the course
        :param category: the category of the course
        :return: an instance of one of Course subclasses
        """
        return CourseFactory.create(type_, name, category)

    def get_course(self, name: str) -> (Course, None):
        """
        Tries to fetch a course by name. If nothing has been found
        returns None instead.

        :param name: name of the course in string format
        :return: either an instance of one of Course subclasses or None
        """
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name: str) -> (Student, None):
        """
        Tries to fetch a student by name. If nothing has been found
        returns None instead.

        :param name: name of the student in string format
        :return: either an instance of Student or None
        """
        for student in self.students:
            if student.name == name:
                return student
        return None
