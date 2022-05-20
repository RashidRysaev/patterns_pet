from views import NotFoundPageView


class App:
    """
    The core class of the framework.
    Takes in the dict with url-patterns and the list of
    front-controllers and then checks for what HTML-page to show
    based on the path.
    """

    def __init__(self, urls, controllers):
        """
        :param urls: url paths
        :param fronts: front controllers
        """
        self.urls = urls
        self.front_controllers = controllers
        self.request = {}

    def __call__(self, environment, start_response):
        """
        :param environment:
        :param start_response:
        :return:
        """
        path = environment['PATH_INFO']
        if path.endswith('/') and not path == '/':
            path = path[:-1]
            print('You`ve got your easter egg, man!')
        if path in self.urls:
            view = self.urls[path]
            for controller in self.front_controllers:
                controller(self.request)
        else:
            view = NotFoundPageView()
        resp, body = view(self.request)
        start_response(resp, [('Content-Type', 'text/html')])
        return body
