"""
Module with base CBVs used throughout the framework as parent classes for
user's templates.
"""
from core.decorators import debug
from core.templator import render_template
from logs.config import Logger

logger = Logger('console', 'main')


class TemplateView:
    """
    Base template view. It simply renders the template with the given name
    using the 'render_template' function from the framework's templator.
    """
    template_name = 'template.html'

    @debug
    def get_context_data(self) -> dict:
        """
        Returns the dictionary with the context data for further rendering.
        """
        return {}

    @debug
    def get_template(self) -> str:
        """
        Returns the template's HTML-file name.
        """
        return self.template_name

    @debug
    def render_template_with_context(self) -> (str, list):
        """
        Renders the template with the given name and given context data.
        """
        template_name = self.get_template()
        context_data = self.get_context_data()
        return '200 Ok', [render_template(
            template_name, **context_data).encode('utf-8')]

    @debug
    def __call__(self, request: dict) -> (str, list):
        """
        Main callable method that renders the template with the given
        context data

        :param request: HTTP request
        :return: rendered template page
        """
        logger.logger(f'Rendering template: {self.template_name} '
                      f'for {self.__class__.__name__}')
        return self.render_template_with_context()


class ListView(TemplateView):
    """
    Base view for a list of objects. Takes in the template name, the
    queryset of the objects and the name of this queryset for use in
    the template itself.
    """
    template_name = 'list.html'
    queryset = []
    context_objects_name = 'objects_list'

    @debug
    def get_queryset(self) -> list:
        """
        Returns the queryset.
        """
        return self.queryset

    @debug
    def get_context_objects_name(self) -> str:
        """
        Returns the name of the objects list for context data.
        """
        return self.context_objects_name

    @debug
    def get_context_data(self) -> dict:
        """
        Returns the context data for further rendering.
        """
        queryset = self.get_queryset()
        context_objects_name = self.get_context_objects_name()
        context = {context_objects_name: queryset}
        return context


class CreateView(TemplateView):
    """
    Base view for the creation of anything. Takes in the name of the
    template, and extracts the request data from POST requests.
    """
    template_name = 'create.html'

    @debug
    def get_request_data(self, request: dict) -> dict:
        """
        Returns the data from the POST request

        :param request: HTTP-request
        """
        return request['data']

    @debug
    def create_object(self, data: dict):
        """
        Creates a new object from the given data.

        :param data: data from the POST-request
        """
        pass

    @debug
    def __call__(self, request: dict) -> (str, list):
        """
        Main callable method. Handles the requests. If it's a POST
        request, creates a new object. Otherwise, just calls on the
        parent's (TemplateView) method to render the template.

        :param request: HTTP-request
        """
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)
