"""
module with helper functions
"""
import requests
from base64 import b64encode
import datetime
import random
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render

unique_id = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100, 999)}"  # Example: '20231125154054_7548'

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
