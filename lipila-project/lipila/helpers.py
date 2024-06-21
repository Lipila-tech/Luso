"""
lipila app Helper Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render
from lipila.models import (
    ContactInfo, HeroInfo, CustomerMessage, UserTestimonial, AboutInfo)
from django.contrib.auth.models import User
from rest_framework.response import Response
import requests
from django.urls import reverse
from api.views import LipilaDisbursementView


def query_collection(user, method, data={}):
    """
    Queries the lipila api payments endpoint for a specific api user.

    Args:
        user (str): The username of the api user.
        method (str): The HTTP method allowed values (GET, POST)
        data (dict): Data to be sent in the POST request.
    Returns:
        rest_framework.response.Response: Response object.
    """
    url = "http://localhost:8000/api/v1/payments/"
    params = {
        "api_user": user,
    }
    if method == 'GET':
        response = requests.get(url, params=params)
        return response
    elif method == 'POST':
        response = requests.post(url, data=data, params=params)
        if response.status_code == 202:
            return Response({'data': 'request accepted, wait for client approval'}, status=202)
        elif response.status_code == 403:
            status_code = response.status_code
            return Response({'data': 'Request exceeded'}, status=status_code)
        elif response.status_code == 400:
            status_code = response.status_code
            return Response({'data': 'Bad request to payment gateway'}, status=status_code)
    else:
        return Response({'data': 'Invalid method passed'}, status=400)


def query_disbursement(user, method, data={}):
    """
    Queries the lipila api disburse endpoint for a specific api user.

    Args:
        user (str): The username of the api user.
        method (str): The HTTP method allowed values (GET, POST)
        data (dict): Data to be sent in the POST request.
    Returns:
        rest_framework.response.Response: Response object.
    """
    url = "http://localhost:8000/api/v1/disburse/"
    params = {
        "api_user": user,
    }
    if method == 'GET':
        response = requests.get(url, params=params)
        return response
    elif method == 'POST':
        response = requests.post(url, data=data, params=params)
        if response.status_code == 202:
            return Response({'data': 'request accepted, wait for client approval'}, status=202)
        elif response.status_code == 403:
            status_code = response.status_code
            return Response({'data': 'Request exceeded'}, status=status_code)
        elif response.status_code == 400:
            status_code = response.status_code
            return Response({'data': 'Bad request to payment gateway'}, status=status_code)
    else:
        return Response({'data': 'Invalid method passed'}, status=400)


def get_lipila_contact_info() -> dict:
    """ Gets the lipila contact info and
    returns a dict object.
    """
    data = {'contact': ''}
    try:
        contact_info = ContactInfo.objects.latest()
        data['contact'] = contact_info
    except ContactInfo.DoesNotExist:
        pass
    return data


def get_user_emails():
    """
    Get all user messages.
    """
    data = {'user_messages': ''}
    try:
        user_messages = CustomerMessage.objects.all()
        data['user_messages'] = user_messages
    except CustomerMessage.DoesNotExist:
        pass
    return data


def get_lipila_index_page_info() -> dict:
    """
    Get the index page info.
    """
    data = {'lipila': ''}
    try:
        lipila_index_info = HeroInfo.objects.latest()
        data['lipila'] = lipila_index_info
    except HeroInfo.DoesNotExist:
        pass
    return data


def get_lipila_about_info() -> dict:
    """
    Get the about info.
    """
    data = {'about': ''}
    try:
        lipila_about_info = AboutInfo.objects.latest()
        data['about'] = lipila_about_info
    except AboutInfo.DoesNotExist:
        pass
    return data


def get_testimonials() -> dict:
    """
    Get testimonials and return a dict object.
    """
    data = {'testimonials': ''}
    try:
        results = UserTestimonial.objects.all()
        data['testimonials'] = results
    except UserTestimonial.DoesNotExist:
        pass
    return data


def get_user_object(user: str):
    """
    Gets a user object from the database.

    Args:
        user: The user object to check.

    Returns:
        A user_object instance(BusinessUser or CreatorProfile or LipilauSE or)
         otherwise returns 404.
    """
    data = {}
    try:
        user_object = User.objects.get(username=user)
        return user_object
    except User.DoesNotExist:
        return None


def apology(request, data=None, user=None):
    """
    Renders a custom error page with the provided data.

    Args:
        request: The Django request object.
        data: A dictionary of data variables to pass to the template.

    Returns:
        An HttpResponseNotFound object with the rendered 404 template.
    """

    template_name = 'lipila/pages/pages_error.html'

    if data is None:
        data = {}

    if data['status'] == 404:
        return HttpResponseNotFound(
            render(request, template_name, data)
        )
    elif data['status'] == 400:
        return HttpResponseBadRequest(
            render(request, template_name, data)
        )
