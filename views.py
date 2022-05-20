from template_renderer import render_template


class IndexPageView:
    """
    Simple view rendering the index page.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
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
        return '200 Ok', [render_template(
            'templates/about.html').encode('utf-8')]


class NotFoundPageView:
    """
    Simple view rendering an non-existing page.
    """

    def __call__(self, request):
        """
        :param request: HTTP-request
        :return: tuple, first element is string, second - list with bytes
        """
        return '404 NOT FOUND', [b'Page not found!']
