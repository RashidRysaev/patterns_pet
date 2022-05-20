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
        request_method = environment['REQUEST_METHOD']
        query_string = environment['QUERY_STRING']
        path = environment['PATH_INFO']
        if path.endswith('/') and not path == '/':
            path = path[:-1]
        data = get_wsgi_input_data(environment)
        data = parse_wsgi_input_data(data)
        request_parameters = parse_input_data(query_string)
        if path in self.urls:
            view = self.urls[path]
            self.request['req_params'] = request_parameters
            self.request['data'] = data
            self.request['method'] = request_method
            for controller in self.front_controllers:
                controller(self.request)
        else:
            view = NotFoundPageView()
        resp, body = view(self.request)
        start_response(resp, [('Content-Type', 'text/html')])
        return body


def parse_input_data(data):
    """
    Receives data from a query string.

    :param data: raw query string
    :return: query data as dict
    """
    result = {}
    if data:
        parameters = data.split('&') # i.e. ?12+2=14&18-3=15 -> ['12+2=14', '18-3=15']
        for item in parameters:
            key, value = item.split('=')
            result[key] = value
    return result # i.e {'12+2': '14', '18-3': '15'}


def get_wsgi_input_data(environment):
    """
    Retrieves the data from the wsgi.input field of a POST-request.

    :param environment: dictionary with all the data
    :return: data encoded in bytes
    """
    query_content_length = environment.get('CONTENT_LENGTH')
    content_length = int(query_content_length) if query_content_length else 0
    data = environment['wsgi.input'].read(content_length) \
        if content_length > 0 else b''
    return data


def parse_wsgi_input_data(raw_data):
    """
    Converts the data from a POST-request to a dictionary.

    :param raw_data: raw input data
    :return: dictionary with values
    """
    result = {}
    if raw_data:
        result = parse_input_data(raw_data.decode('utf-8'))
    return result
