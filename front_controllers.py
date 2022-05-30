def front_controller(request):
    """
    A simple front controller that just changes one thing in context.

    :param request: HTTP-request
    """
    request['keyword'] = 'Oi mate!'