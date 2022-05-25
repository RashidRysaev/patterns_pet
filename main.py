from core import App
from views import IndexPageView, AboutPageView, ContactPageView


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
}

controllers = [
    front_controller
]

app = App(routes, controllers)
