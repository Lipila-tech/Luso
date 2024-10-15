"""
lipila app Util Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from lipila.models import (
    ContactInfo, HeroInfo, CustomerMessage, UserTestimonial, AboutInfo)
from django.conf import settings
from rest_framework.response import Response
import requests
from django.urls import reverse
from api.models import MomoColTransaction, MomoDisTransaction
from django.contrib.auth import get_user_model
import braintree
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from accounts.models import CreatorProfile
from patron.models import TierSubscriptions, Tier
from api.utils import generate_transaction_id
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect


def get_tier_subscription_by_id_patron(id, patron):
    subscription = get_object_or_404(TierSubscriptions, tier=id, patron=patron)
    return subscription


def get_tier_by_patron_title(title: str)-> Tier:
    """
    Retrives a tier matching a creator.

    Args:
        title(str): A Creators patron_title

    Returns:
        A Tier Object.
    """
    creator = get_object_or_404(CreatorProfile, patron_title=title)
    tier = get_object_or_404(Tier, creator=creator )
    return tier

def get_creator_by_patron_title(patron_title):
    creator_profile = get_object_or_404(CreatorProfile, patron_title=patron_title)
    return creator_profile.user


def get_patron_profile_by_patron_title(patron_title):
    profile = get_object_or_404(CreatorProfile, patron_title=patron_title)
    return profile


def get_patron_title_by_creator(creator):
    patron_title = get_object_or_404(CreatorProfile, user=creator)
    return patron_title


def is_patron_title_valid(title: str)-> bool:
    """
    Looks up a provide string in the database.

    Args:
        title(str): The name of a Patron title to search for.

    Returns:
        True if found, else False.
    """

    try:
        get_object_or_404(CreatorProfile, patron_title=title)
        return True
    except Http404:
        return False


def get_customer_id(user):
    """
    returns the id of the user.
    """

    return get_user_model().objects.get(username=user).id


braintree_gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY
    )
)


def get_braintree_client_token(user: str)-> dict:
    """
    Generates a client token that contains all authorization and configuration
    information the client needs to initialize the client SDK to communicate with Braintree.

    Args:
        user(str): The user name of a client we are generating the token for.

    Returns:
        client_token as dict object with `customer_id` as key.
    """
    client_token = braintree_gateway.client_token.generate()
    return client_token


def get_api_user():
    return get_user_model().objects.get(username='lipila')


def query_collection(user, method, transaction_id, data={}):
    """
    Queries the lipila api payments endpoint for a specific api user.

    Args:
        user (str): The username of the api user.
        method (str): The HTTP method allowed values (GET, POST)
        transaction_id(str): The unique uuid id that will be used to identify the transactions
        data (dict): data (dict):
                {
                    'amount': '', 'msisdn': '',
                    'wallet_type': '', 'reference': ''
                    }

    Returns:
        rest_framework.response.Response: Response object.
    """
    url = "http://localhost:8000/api/v1/payments/"
    params = {
        "api_user": user,
        "transaction_id": transaction_id
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


def query_disbursement(user, method, transaction_id, data={}):
    """
    Queries the lipila api disburse endpoint for a specific api user.

    Args:
        user (str): The username of the api user.
        method (str): The HTTP method allowed values (GET, POST)
        transaction_id(str): The unique uuid id that will be used to identify the transactions
        data (dict):
                {
                    'amount': '', 'send_money_to': '',
                    'wallet_type': '', 'reference': ''
                    }

    Returns:
        rest_framework.response.Response: Response object.
    """
    url = "http://localhost:8000/api/v1/disburse/"
    params = {
        "api_user": user,
        "transaction_id": transaction_id
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


def check_payment_status(transaction_id: str, transaction: str) -> str:
    """
    This function checks the status of the transaction in the api models.

    Args:
        transaction_id(str): The uuid that identifies the transaction.
        transaction(str): The type of transaction to check. options are (col, dis)

    Returns: status (str) options [success, failed, pending]
    """
    status = ''
    if transaction == 'col':
        try:
            status = MomoColTransaction.objects.get(
                transaction_id=transaction_id).status

        except MomoColTransaction.DoesNotExist:
            status = 'transaction id not found'
    elif transaction == 'dis':
        try:
            status = MomoDisTransaction.objects.get(
                transaction_id=transaction_id).status

        except MomoDisTransaction.DoesNotExist:
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
        user_object = get_user_model().objects.get(username=user)
        return user_object
    except get_user_model().DoesNotExist:
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
    elif data['status'] == 500:
        return HttpResponseServerError(
            render(request, template_name, data)
        )


# Process payment
# Define variables
def process_mtn_payment(*args, **kwargs):
    amount = kwargs.pop('amount')
    msisdn = kwargs.pop('msisdn')
    reference = kwargs.pop('reference')
    transaction_id = kwargs.pop('transaction_id')

    # Populate fields
    
    payload = {
        'amount': amount,
        'wallet_type': 'mtn',
        'msisdn': msisdn,
        'reference': reference
    }

    api_user = get_api_user()

    response = query_collection(
        api_user.username, 'POST', transaction_id, data=payload)
    if response.status_code == 202:
        if check_payment_status(transaction_id, 'col') == 'success':
                return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'waiting user for user response'}, status=202)
    else:
        return JsonResponse({'message': 'Bad request', 'status':'failed'}, status=400)
        