"""
Module that renders the templates. The main function here
takes in the name of the template, the folder the templates are stored in
and any keyword arguments you might want to pass into the template, and then
renders the HTML-page with the help of Jinja2.
"""
from jinja2 import Environment, FileSystemLoader


def render_template(template_name, **kwargs) -> str:
    """
    Function that renders the templates using Jinja2.

    :param template_name: name of html-file
    :param kwargs: any data passed into template
    :return: rendered HTML template
    """
    with open(template_name, encoding='utf-8') as temp:
        template = temp.read()
        template = Environment(loader=FileSystemLoader(
            'templates/')).from_string(template)
    return template.render(**kwargs)
