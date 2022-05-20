from datetime import datetime

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
        if request['method'] == 'POST':
            self.save_to_file(request)
            return '200 Ok', [render_template(
                'templates/contact.html').encode('utf-8')]
        else:
            return '200 Ok', [render_template(
                'templates/contact.html').encode('utf-8')]

    
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
