"""
Util Functions
"""
from django.contrib.auth import get_user_model
import requests
from base64 import b64encode
from django.conf import settings
from rest_framework.response import Response
import datetime
import random
from uuid import uuid4
import os

unique_id = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100, 999)}"
User = settings.AUTH_USER_MODEL


import openapi_client
from openapi_client.models.payment_request import PaymentRequest
from openapi_client.models.payment_response import PaymentResponse
from openapi_client.rest import ApiException
from pprint import pprint


def create_payment():
    # Defining the host is optional and defaults to https://api.mtn.com/v1
    # See configuration.py for a list of all supported configuration parameters.
    configuration = openapi_client.Configuration(
        host = "https://api.mtn.com/v1"
    )

    # The client must configure the authentication and authorization parameters
    # in accordance with the API server security policy.
    # Examples for each auth method are provided below, use the example that
    # satisfies your auth use case.

    configuration.access_token = os.environ["ACCESS_TOKEN"]

    # Enter a context with an instance of the API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        c_id=1
        t_type ='payment'
        c_URL= 'http://localhost://accouts/mtn/callback'
        t_amount='120'
        p_method=''

        api_instance = openapi_client.SubmitPaymentOrRefundRequestApi(api_client)
        payment_request = openapi_client.PaymentRequest(correlatorId=c_id, transactionType=t_type, callbackURL=c_URL,totalAmount=t_amount, paymentMethod=p_method)
        x_authorization = 'x_authorization_example' # str | Encrypted ECW credentials (optional)

        try:
            # Provides the ability for a consumer to make a payment or refund to service providers.
            api_response = api_instance.create_payment(payment_request, x_authorization=x_authorization)
            print("The response of SubmitPaymentOrRefundRequestApi->create_payment:\n")
            pprint(api_response)
        except Exception as e:
            print("Exception when calling SubmitPaymentOrRefundRequestApi->create_payment: %s\n" % e)


def get_api_user(user:str)-> User:
    """
    This function reteives a user registered as a api user.

    Args:
        user(str): The user of the user to get.

    Returns:
        A User obeject.
    """
    try:
        user = get_user_model().objects.get(username=user)
        return user
    except get_user_model().DoesNotExist:
        return Response({"error": "api user not found"}, status=404)



def generate_transaction_id():
  return str(uuid4())
        

def basic_auth(username:str, password:str):
    """
    generates a Basic Authorization token: we need to encode it to base64 
    and then decode it to acsii as python 3 stores it as a byte string
    params:
        username: momo x_transaction_id
        password: momo apikey
    """
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def is_payment_details_valid(*args, **kwargs):
    """
    Checks the validity of payment details, accepting either positional arguments or keyword arguments.

    Args:
        *args (tuple): Positional arguments, expected to be (amount, payer, reference) in order.
        **kwargs (dict): Keyword arguments with keys 'amount', 'payer', and/or 'reference'.

    Returns:
        bool: True if all details are valid, False otherwise.

    Raises:
        TypeError: If any argument is not a string.
        ValueError: If amount is less than 10 or party_id is not 10 digits long.
    """
    try:
        valid_keys = {'amount', 'payer', 'reference'}
        # details = {key: value for key, value in (kwargs.items() if kwargs else args)}  # Combine args and kwargs
        details = {key: value for key, value in zip(['amount', 'payer', 'reference'], args)}
        if len(details) != 3 or not all(key in valid_keys for key in details):
            raise ValueError("Missing or invalid arguments. Expected 'amount', 'payer', and 'reference'.")

        for key, value in details.items():
            if not isinstance(value, str):
                raise TypeError(f"Argument '{key}' must be a string.")

        if float(details['amount']) < 10.0 or len(details['payer']) < 9:
            raise ValueError("Amount must be greater than 10 and payer must be 10 digits long.")
        if ' ' in (details['reference']):
            raise ValueError("Reference should not contain spaces.")
    except AssertionError:
        raise ValueError("Missing or invalid arguments. Expected 'amount', 'payer', and 'reference'.")
    return True

def is_deposit_details_valid(*args, **kwargs):
    """
    Checks the validity of payment details, accepting either positional arguments or keyword arguments.

    Args:
        *args (tuple): Positional arguments, expected to be (amount, payer, reference) in order.
        **kwargs (dict): Keyword arguments with keys 'amount', 'payer', and/or 'reference'.

    Returns:
        bool: True if all details are valid, False otherwise.

    Raises:
        TypeError: If any argument is not a string.
        ValueError: If amount is less than 10 or party_id is not 10 digits long.
    """
    try:
        valid_keys = {'amount', 'payee', 'reference'}
        # details = {key: value for key, value in (kwargs.items() if kwargs else args)}  # Combine args and kwargs
        details = {key: value for key, value in zip(['amount', 'payee', 'reference'], args)}
        if len(details) != 3 or not all(key in valid_keys for key in details):
            raise ValueError("Missing or invalid arguments. Expected 'amount', 'payee', and 'reference'.")

        for key, value in details.items():
            if not isinstance(value, str):
                raise TypeError(f"Argument '{key}' must be a string.")

        if float(details['amount']) < 10.0 or len(details['payee']) < 9:
            raise ValueError("Amount must be greater than 10 and payer must be 10 digits long.")
        if ' ' in (details['reference']):
            raise ValueError("Reference should not contain spaces.")
    except AssertionError:
        raise ValueError("Missing or invalid arguments. Expected 'amount', 'payee', and 'reference'.")
    return True
