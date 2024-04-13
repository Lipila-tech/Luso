"""
Helper Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render
from api.models import BusinessUser


def apology(request, context=None, user=None):
    """
    Renders a custom error page with the provided context.

    Args:
        request: The Django request object.
        context: A dictionary of context variables to pass to the template.

    Returns:
        An HttpResponseNotFound object with the rendered 404 template.
    """

    template_name = 'pages-error.html'

    if context is None:
        context = {}

    if context['status'] == 404:
        return HttpResponseNotFound(
            render(request, template_name, context)
        )
    elif context['status'] == 400:
        return HttpResponseBadRequest(
            render(request, template_name, context)
        )


def set_context(request, user):
    context = {}
    try:
        if not user:
            raise ValueError('Username missing')
        else:
            user = BusinessUser.objects.get(username=user)
            context['status'] = 200
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context)
    except BusinessUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context)
    return context