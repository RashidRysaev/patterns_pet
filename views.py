from datetime import datetime

from template_renderer import render_template
from logs.config import Logger
from models import OnlineUniversity

site = OnlineUniversity()
logger = Logger('main')


class IndexPageView:
    """
    Simple view rendering the index page.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
        logger.logger(f'{__name__}.py; IndexView; requested index page.')
        keyword = request.get('keyword', None)
        return '200 Ok', [render_template('templates/index.html',
                                        keyword=keyword).encode('utf-8')]


class AboutPageView:
    """
    Simple view rendering the about page.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
        logger.logger(f'{__name__}.py; AboutView; requested about page.')
        return '200 Ok', [render_template(
            'templates/about.html').encode('utf-8')]


class ContactPageView:
    """
    Simple view rendering the contact form page.
    """

    def __call__(self, request):
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
        logger.logger(f'{__name__}.py; ContactPageView; requested Contacts page.')
        if request['method'] == 'POST':
            self.save_to_file(request)
            return '200 Ok', [render_template(
                'templates/contact.html').encode('utf-8')]
        else:
            return '200 Ok', [render_template(
                'templates/contact.html').encode('utf-8')]

    @staticmethod
    def save_to_file(self, request):
        """
        Saves data from incoming POST-request to file.

        :param request: incoming data
        """
        with open(f"incoming_msg_{datetime.now()}", 'w') as f:
            text = f"Incoming message:\n\n" \
                f"From: {request['data']['email']};\n" \
                f"Subject: {request['data']['subject']};\n" \
                f"Text:\n{request['data']['message_text']}"
            f.write(text)
            f.close()


class CoursesListView:
    """
    Class-based view for a list of all available courses.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second HTML-code
        """
        logger.logger(
            f'{__name__}.py; CoursesListView; requested the list of courses.')
        return '200 Ok', [render_template(
            'templates/courses_list.html',
            objects_list=site.courses).encode('utf-8')]


class CreateCourseView:
    """
    Class-based view for the course creation page.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        logger.logger(
            f'{__name__}.py: CreateCourseView; requested course creation.')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            cat_id = data.get('category_id')
            category = None
            if cat_id:
                category = site.find_category(int(cat_id))
                new_course = site.create_course('online', name, category)
                site.courses.append(new_course)
            return '200 Ok', [render_template(
                'templates/create_course.html').encode('utf-8')]
        else:
            categories = site.course_categories
            return '200 Ok', [render_template(
                'templates/create_course.html',
                categories=categories).encode('utf-8')]


class CopyCourseView:
    """
    Class-based view to handle the copying of a course.
    """

    def __call__(self, request):
        """
        Main callable method. Handles the copying of a given
        course by invoking a Prototype Mixin method 'clone'.
        :param request: HTTP-requests
        :return: tuple, first element is string, second HTML code
        """
        #params = request['params']
        params = request.get('request_params', None)
        print(params)
        name = params['name']
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


class CategoryListView:
    """
    Class-based view for the list of existing course categories.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second HTML-code
        """
        logger.logger(
            f'{__name__}.py; CategoryListView; '
            f'requested the list of course categories.')
        return '200 Ok', [render_template(
            'templates/categories_list.html',
            objects_list=site.course_categories).encode('utf-8')]


class CreateCategoryView:
    """
    Class-based view for a category creation page.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        logger.logger(
            f'{__name__}.py; CreateCategoryView; creating new category.')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            cat_id = data.get('category_id')
            category = None
            if cat_id:
                category = site.find_category(int(cat_id))
            new_category = site.create_category(name, category)
            site.course_categories.append(new_category)
            return '200 Ok', [render_template(
                'templates/create_category.html').encode('utf-8')]
        else:
            categories = site.course_categories
            return '200 Ok', [render_template(
                'templates/create_category.html',
                categories=categories).encode('utf-8')]

