"""
The core module of the WSGI framework. Contains the main Application
class for the framework and also several subclasses for logging and testing.
"""
from quopri import decodestring
from typing import Callable
from wsgiref.util import setup_testing_defaults


class Application:
    """
    The core class of the WSGI framework.
    """

    def __init__(self, urls: dict, fronts: list):
        """
        Takes in the dict with url-patterns and the list of front controllers.

        :param urls: url paths
        :param fronts: front controllers
        """
        self.urls = urls
        self.front_controllers = fronts
        self.request = {}

    def __call__(self, environment: dict, start_response: Callable) -> list:
        """
        Main callable method of the class. Does all the work:
        analyzes the HTTP-request and then chooses an appropriate view
        based on the URL path given.

        :param environment:
        :param start_response:
        :return:
        """
        setup_testing_defaults(environment)
        request_method = environment['REQUEST_METHOD']
        query_string = environment['QUERY_STRING']
        path = environment['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        data = self.get_wsgi_input_data(environment)
        data = self.parse_wsgi_input_data(data)
        request_parameters = self.parse_input_data(query_string)
        if path in self.urls:
            view = self.urls[path]
            self.request['method'] = request_method
            self.request['data'] = data
            self.request['req_params'] = request_parameters
            for controller in self.front_controllers:
                controller(self.request)
            resp, body = view(self.request)
            start_response(resp, [('Content-Type', 'text/html')])
            return body
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'PAGE NOT FOUND']

    @staticmethod
    def parse_input_data(data: str) -> dict:
        """
        Receives data from a query string.

        :param data: raw query string
        :return: query data in a form of dictionary
        """
        result = {}
        if data:
            parameters = data.split('&')
            for item in parameters:
                key, value = item.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_wsgi_input_data(environment: dict) -> bytes:
        """
        Retrieves the data from the wsgi.input field of a POST-request.

        :param environment: dictionary with all the data
        :return: data encoded in bytes
        """
        query_content_length = environment.get('CONTENT_LENGTH')
        content_length = int(
            query_content_length) if query_content_length else 0
        data = environment['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, raw_data: bytes) -> dict:
        """
        Converts the data from a POST-request to a dictionary.

        :param raw_data: raw input data
        :return: dictionary with values
        """
        result = {}
        if raw_data:
            data_string = self.decode_value(raw_data.decode('utf-8'))
            result = self.parse_input_data(data_string)
        return result

    @staticmethod
    def decode_value(value: str) -> str:
        """
        Correctly decodes bytes with Cyrillic text correctly.

        :param value: string to decode
        :return: decoded string
        """
        bytes_value = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
        decoded_string = decodestring(bytes_value)
        return decoded_string.decode('UTF-8')


class LoggingApplication(Application):
    """
    Logging subclass. Everything it does is the same, except it
    prints some useful information in stdout.
    """

    def __init__(self, urls: dict, fronts: list):
        """
        The Application subclass for logging. First creates the main
        application for future purposes, then calls the super.__init__
        of the parent.

        :param urls: url paths
        :param fronts: front controllers
        """
        self.app = Application(urls, fronts)
        super().__init__(urls, fronts)

    def __call__(self, environment: dict, start_response: Callable) -> list:
        """
        The main callable method of the subclass. Does everything the same
        as the respective method in the parent class with the addition
        of logging. Prints in the stdout the following info: url path,
        request method and the query string for GET-requests.

        :param environment:
        :param start_response:
        """
        print('LOGGING APP')
        print(f"******************************************\n"
              f"PATH_INFO: {environment['PATH_INFO']};\n"
              f"REQUEST_METHOD: {environment['REQUEST_METHOD']};\n"
              f"QUERY_STRING: {environment['QUERY_STRING']};\n"
              f"******************************************"
              )
        return self.app(environment, start_response)


class SpoofApplication(Application):
    """
    Dummy application subclass. Does nothing but return one phrase for
    any request it receives.
    """

    def __init__(self, urls: dict, fronts: list):
        """
        Dummy application subclass. Does nothing but return one phrase for
        any request it receives.

        :param urls: url routes
        :param fronts: front controllers
        """
        self.app = Application(urls, fronts)
        super().__init__(urls, fronts)

    def __call__(self, environment: dict, start_response: Callable) -> list:
        """
        Main callable method. Returns just one phrase for any request.

        :param environment:
        :param start_response:
        """
        start_response('200 Ok', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
