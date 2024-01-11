"""
module with helper functions
"""
import requests
from base64 import b64encode

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