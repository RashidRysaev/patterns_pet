from core import App
from views import IndexPageView, AboutPageView, ContactPageView, CoursesListView, CreateCourseView, CopyCourseView, CategoryListView, CreateCategoryView


def front_controller(request):
    """
    A simple front controller that just changes one thing in context.

    :param request: HTTP-request
    """
    request['keyword'] = 'Oi mate!'


routes = {
    '/': IndexPageView(),
    '/about': AboutPageView(),
    '/contact': ContactPageView(),
    '/all_courses': CoursesListView(),
    '/create_course': CreateCourseView(),
    '/copy_course': CopyCourseView(),
    '/all_categories': CategoryListView(),
    '/create_category': CreateCategoryView(),
}

controllers = [
    front_controller
]

app = App(routes, controllers)
