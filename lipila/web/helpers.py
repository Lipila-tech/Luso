"""
Helper Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render


def apology(request, context=None):
    """
    Renders a custom error page with the provided context.

    Args:
        request: The Django request object.
        context: A dictionary of context variables to pass to the template.

    Returns:
        An HttpResponseNotFound object with the rendered 404 template.
    """

    template_name = 'AdminUI/pages-error.html'  # Customize this to your template name

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
