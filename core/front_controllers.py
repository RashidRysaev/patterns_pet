"""
Module with the front controllers for the framework.
"""


def front_controller(request: dict):
    """
    A simple front controller that just changes one thing in context.
    For now!

    :param request: HTTP-request
    """
    request['keyword'] = 'ЖИЖНЯ!'
