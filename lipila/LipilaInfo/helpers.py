"""
Helper Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, get_list_or_404
from business.models import BusinessUser
from creators.models import CreatorUser
from LipilaInfo.models import LipilaUser, Patron, ContactInfo


def get_lipila_contact_info():
    context = {}
    try:
        contact_info = ContactInfo.objects.get(id=1)
        context['street'] = contact_info.street
        context['location'] = contact_info.location
        context['phone3'] = contact_info.phone1
        context['phone2'] = contact_info.phone2
        context['email1'] = contact_info.email1
        context['email2'] = contact_info.email2
        context['days'] = contact_info.days
        context['hours'] = contact_info.hours
    except ContactInfo.DoesNotExist:
        context['street'] = ''
        context['location'] = ''
        context['phone3'] = ''
        context['phone2'] = ''
        context['email1'] = ''
        context['email2'] = ''
        context['days'] = ''
        context['hours'] = ''

    return context

def get_patrons(user_type: str, user:str):
    """
    Gets a users patrons

    Args:
        user_type: The user category
        user: The user object to get patrons for.

    Returns:
        A patron_object.
    """
    try:
        if user_type == "creator":
            creator_object = Patron.objects.filter(creator=user)
            return creator_object.count()
        elif user_type == "member":
            patron_object = Patron.objects.filter(username=user)
            return patron_object.count()
    except Patron.DoesNotExist:
        return 0
    

def get_user_object(user: str):
    """
    Gets a user object from the database.

    Args:
        user: The user object to check.

    Returns:
        A user_object instance(BusinessUser or CreatorUser or LipilauSE or)
         otherwise returns 404.
    """
    context = {}
    try:
        user_object = BusinessUser.objects.get(username=user)
        return user_object
    except BusinessUser.DoesNotExist:
        pass  # Continue to next check
    try:
        user_object = CreatorUser.objects.get(username=user)
        patrons = get_patrons('creator', user_object)
        return user_object, patrons
    except CreatorUser.DoesNotExist:
        pass  # Continue to next check
    try:
        user_object = LipilaUser.objects.get(username=user)
        patrons = get_patrons('member', user_object)
        return user_object, patrons
    except LipilaUser.DoesNotExist:
        context['status'] = 404
        return context

def check_if_user_is_patron(user, creator):
    """Checks is a user is already a patron
    if yes returns False else returns True.
    """
    is_patron = False
    try:
        creator_obj = get_user_object(creator)
        user_object = Patron.objects.filter(username=user)
        patron = Patron.objects.filter(creator=creator_obj[0])
        is_patron = True
    except Patron.DoesNotExist:
        is_patron = False
    return is_patron


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