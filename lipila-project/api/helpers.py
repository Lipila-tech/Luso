"""
Helper Functions
"""
import requests
from base64 import b64encode
from django.contrib.auth.models import User
from rest_framework.response import Response
import datetime
import random
unique_id = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100, 999)}"  # Example: '20231125154054_7548'



def get_api_user(user:str)-> User:
    """
    This function reteives a user registered as a api user.

    Args:
        user(str): The user of the user to get.

    Returns:
        A User obeject.
    """
    try:
        user = User.objects.get(username=user)
        return user
    except User.DoesNotExist:
        return Response({"error": "api user not found"}, status=404)


def get_uuid4() -> str:
        """
        Method that generates a uuid4(x_reference_id) number
        """
        url = "https://www.uuidgenerator.net/api/version4"
        payload = {}
        headers = {}
        try:
            response = requests.get(url, headers=headers, data=payload)
            return response.text
        except Exception:
            return "none"
        

def basic_auth(username:str, password:str):
    """
    generates a Basic Authorization token: we need to encode it to base64 
    and then decode it to acsii as python 3 stores it as a byte string
    params:
        username: momo x_reference_id
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

        if int(details['amount']) < 10 or len(details['payer']) != 10:
            raise ValueError("Amount must be greater than 10 and payer must be 10 digits long.")
        if ' ' in (details['reference']):
            raise ValueError("Reference should not contain spaces.")
    except AssertionError:
        raise ValueError("Missing or invalid arguments. Expected 'amount', 'payer', and 'reference'.")
    return True
