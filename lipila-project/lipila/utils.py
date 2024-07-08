"""
lipila app Util Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render
from lipila.models import (
    ContactInfo, HeroInfo, CustomerMessage, UserTestimonial, AboutInfo)
from django.contrib.auth.models import User
from rest_framework.response import Response
import requests
from django.urls import reverse
from api.models import LipilaCollection, LipilaDisbursement



# utils.py

from patron.models import Contributions, SubscriptionPayments, Transfer

def save_payment(model_class, **kwargs):
    """
    Saves a payment to the database options are [contribution, payment, transfer].

    Args:
        model_class(cls): The model class where a transaction should be saved.
        kwargs(dict): The data to be saved

    Returns:
        a payment object.
    """
    reference_id = kwargs.get('reference_id')
    amount = kwargs.get('amount')
    payer_account_number = kwargs.get('payer_account_number')
    payee_account_number=kwargs.get('payee_account_number')
    network_operator = kwargs.get('network_operator')
    description = kwargs.get('description')
    patron = kwargs.get('patron')
    payee = kwargs.get('payee')
    payer = kwargs.get('payer')
    

    payment = model_class.objects.create(
        reference_id=reference_id,
        amount=amount,
        payer_account_number=payer_account_number,
        network_operator=network_operator,
        description=description,
    )
    payment.save()
    if model_class == Contributions:
        payment.payer = payer
        payment.payee = payee
        payment.save()

    if model_class == SubscriptionPayments:    
        payment.payee = payee
        payment.save()
        
    if model_class == Transfer:
        payment.payer = payer
        payment.payee_account_number = payee_account_number
        payment.save()
    return payment


def query_collection(user, method, reference_id, data={}):
    """
    Queries the lipila api payments endpoint for a specific api user.

    Args:
        user (str): The username of the api user.
        method (str): The HTTP method allowed values (GET, POST)
        reference_id(str): The unique uuid id that will be used to identify the transactions
        data (dict): data (dict):
                {
                    'amount': '', 'payer_account_number': '',
                    'network_operator': '', 'description': ''
                    }
                    
    Returns:
        rest_framework.response.Response: Response object.
    """
    url = "http://localhost:8000/api/v1/payments/"
    params = {
        "api_user": user,
        "reference_id": reference_id
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


def query_disbursement(user, method, reference_id, data={}):
    """
    Queries the lipila api disburse endpoint for a specific api user.

    Args:
        user (str): The username of the api user.
        method (str): The HTTP method allowed values (GET, POST)
        reference_id(str): The unique uuid id that will be used to identify the transactions
        data (dict):
                {
                    'amount': '', 'payee_account_number': '',
                    'network_operator': '', 'description': ''
                    }

    Returns:
        rest_framework.response.Response: Response object.
    """
    url = "http://localhost:8000/api/v1/disburse/"
    params = {
        "api_user": user,
        "reference_id": reference_id
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


def check_payment_status(reference_id:str, transaction:str)->str:
    """
    This function checks the status of the transaction in the api models.

    Args:
        reference_id(str): The uuid that identifies the transaction.
        transaction(str): The type of transaction to check. options are (col, dis)

    Returns: status (str) options [success, failed, pending]
    """
    status = ''
    if transaction == 'col':
        try:
            status = LipilaCollection.objects.get(reference_id=reference_id).status
            
        except LipilaCollection.DoesNotExist:
            status = 'transaction id not found'
    elif transaction == 'dis':
        try:
            status = LipilaDisbursement.objects.get(reference_id=reference_id).status
            
        except LipilaDisbursement.DoesNotExist:
            status = 'transaction id not found'
    else:
        return None
    return status

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
