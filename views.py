"""
Module with class-based views for the project.
"""
from datetime import datetime

from core.bases import BaseSerializer
from core.templator import render_template
from core.views import TemplateView, ListView, CreateView
from core.wsgi_core import Application
from logs.config import Logger
from models import OnlineUniversity, EmailNotifier, TextMessageNotifier
from core.decorators import UrlPaths, debug
from orm.core import UnitOfWork
from orm.mappers import MapperRegistry

site = OnlineUniversity()
email_notifier = EmailNotifier()
text_notifier = TextMessageNotifier()
logger = Logger('file', 'main')
routes = UrlPaths()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@routes.add_route('/api/')
class CoursesApiView:
    def __call__(self, request: dict) -> (str, list):
        logger.logger(f'{__name__}.py; CoursesApiView; sending the list of'
                      f'courses via API.')
        return '200 Ok', [BaseSerializer(site.courses).save().encode('utf-8')]


@routes.add_route('/')
class IndexView(TemplateView):
    """
    Class-based view for an index page. Subclass to TemplateView.
    Main functionality is realized in the parent class.
    """
    template_name = 'templates/index.html'


@routes.add_route('/about/')
class AboutView(TemplateView):
    """
    Class-based view for an about page. Subclass to TemplateView.
    Main functionality is realized in the parent class.
    """
    template_name = 'templates/about.html'


@routes.add_route('/contacts/')
class ContactsView(TemplateView):
    """
    Class-based view for a contacts page. Subclass to TemplateView.
    Since it needs to be able to handle the POST-requests, the __call__
    method has been overridden here.
    """
    template_name = 'templates/contacts.html'

    @staticmethod
    @debug
    def save_to_file(request: dict) -> None:
        """
        Saves data from incoming POST-request to file.

        :param request: incoming data
        """
        try:
            logger.logger('Trying to save the POST-data to file.')
            with open(f"incoming_msg_{datetime.now()}.txt", 'w') as f:
                text = f"Incoming message:\n" \
                       f"From: {request['data']['email']};\n" \
                       f"Subject: {request['data']['header']};\n" \
                       f"Text:\n{request['data']['message']}"
                f.write(text)
                f.close()
        except Exception as e:
            logger.logger(f'Saving to file failed: {e}.')
        else:
            logger.logger('Data saved successfully.')

    @debug
    def __call__(self, request: dict) -> (str, list):
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        if request['method'] == 'POST':
            self.save_to_file(request)
            return '200 Ok', [render_template(
                'templates/contacts.html').encode('utf-8')]
        else:
            return '200 Ok', [render_template(
                'templates/contacts.html').encode('utf-8')]


@routes.add_route('/all_courses/')
class CoursesListView(ListView):
    """
    Class-based view for a list of all available courses.
    Subclass to ListView. Main functionality is realized in the
    parent class.
    """
    template_name = 'templates/courses_list.html'
    queryset = site.courses


@routes.add_route('/create_course/')
class CreateCourseView(CreateView):
    """
    Class-based view for the course creation page.
    """
    template_name = 'templates/create_course.html'

    def get_context_data(self) -> dict:
        """
        Retrieves the context data for the template and updates it
        with the list of existing courses.
        """
        context = super().get_context_data()
        context['categories'] = site.course_categories
        return context

    def create_object(self, data: dict):
        """
        Creates a new course object from the data pulled from
        the POST-request.

        :param data: new course data
        """
        name = data['name']
        name = Application.decode_value(name)
        cat_id = data.get('category_id')
        category = None
        if cat_id:
            category = site.find_category(int(cat_id))
        new_course = site.create_course('online', name, category)
        new_course.observers.append(email_notifier)
        new_course.observers.append(text_notifier)
        site.courses.append(new_course)


@routes.add_route('/copy_course/')
class CopyCourseView:
    """
    Class-based view to handle the copying of a course.
    """

    @debug
    def __call__(self, request: dict) -> (str, list):
        """
        Main callable method. Handles the copying of a given
        course by invoking a Prototype Mixin method 'clone'.

        :param request: HTTP-requests
        :return: tuple, first element is string, second HTML code
        """
        params = request['request_params']
        name = params['name']
        name = Application.decode_value(name)
        logger.logger(
            f'{__name__}.py; CopyCourseView; copying course {name}.')
        old_course = site.get_course(name)
        if old_course:
            new_name = f'{name}_copy'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)
        return '200 Ok', [render_template(
            'templates/course_list.html',
            objects_list=site.courses).encode('utf-8')]


@routes.add_route('/all_categories/')
class CategoryListView(ListView):
    """
    Class-based view for the list of existing course categories.
    Subclass to ListView. Main functionality is realized in the
    parent class.
    """
    template_name = 'templates/categories_list.html'
    queryset = site.course_categories


@routes.add_route('/create_category/')
class CreateCategoryView(CreateView):
    """
    Class-based view for a category creation page.
    """
    template_name = 'templates/create_category.html'

    def get_context_data(self) -> dict:
        """
        Retrieves the context data for the template and updates it
        with the list of existing courses.
        """
        context = super().get_context_data()
        context['categories'] = site.course_categories
        return context

    def create_object(self, data: dict):
        """
        Creates a new course category object from the data pulled from
        the POST-request.

        :param data: new course data
        """
        name = data['name']
        name = Application.decode_value(name)
        cat_id = data.get('category_id')
        category = None
        if cat_id:
            category = site.find_category(int(cat_id))
        new_category = site.create_category(name, category)
        site.course_categories.append(new_category)


@routes.add_route('/all_students/')
class StudentsListView(ListView):
    """
    Class-based view for the list of all students.
    """
    template_name = 'templates/students_list.html'

    def get_queryset(self) -> list:
        """
        Retrieves the queryset from the database.

        :return: all current students
        """
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.return_all()


@routes.add_route('/create_student/')
class StudentCreateView(CreateView):
    """
    Class-based view for the creation of a new student.
    """
    template_name = 'templates/create_student.html'

    def create_object(self, data: dict):
        """
        Creates a new student using the data retrieved from
        the POST-request.

        :param data: new student data
        """
        name = data['name']
        name = Application.decode_value(name)
        new_student = site.create_user('student', name)
        site.students.append(new_student)
        new_student.mark_new()
        UnitOfWork.get_current().commit()


@routes.add_route('/enlist_student/')
class EnlistStudentView(CreateView):
    """
    Class-based view for the enrollment of a student on a course.
    """
    template_name = 'templates/enlist_student.html'

    def get_context_data(self) -> dict:
        """
        Retrieves the context data for the template and updates it
        with the list of existing courses and students.
        """
        context = super().get_context_data()
        context['students'] = site.students
        context['courses'] = site.courses
        return context

    def create_object(self, data: dict):
        """
        Retrieves the course and student's name from the POST-request
        data. Then retrieves the objects for the two. And finally
        enlists the student in the course.

        :param data: POST-request data
        """
        course_name = data['course_name']
        course_name = Application.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = Application.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
