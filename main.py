from core import App
from views import *
from front_controllers import front_controller
from decos import UrlPaths


# routes = {
#     '/': IndexPageView(),
#     '/about': AboutPageView(),
#     '/contact': ContactPageView(),
#     '/all_courses': CoursesListView(),
#     '/create_course': CreateCourseView(),
#     '/copy_course': CopyCourseView(),
#     '/all_categories': CategoryListView(),
#     '/create_category': CreateCategoryView(),
# }

routes = UrlPaths()

controllers = [
    front_controller
]

app = App(routes.URLS, controllers)
