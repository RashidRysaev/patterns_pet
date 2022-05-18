from jinja2 import Environment, FileSystemLoader


def render_template(template_name, **kwargs):
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
