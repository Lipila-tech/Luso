"""
Helper Functions
"""
from base64 import b64encode, b64decode
from django.utils.encoding import force_bytes, force_str


def basic_auth_encode(userid):
    """
    generates a Basic Authorization token: we need to encode it to base64 
    and then decode it to acsii as python 3 stores it as a byte string
    params:
        userid: user pk
    """
    token = b64encode(force_str(userid).encode('utf-8')).decode("ascii")
    return token


def basic_auth_decode(token):
    """
    Decodes a Basic Authorization token.
    params:
        token: The token to decode
    """
    try:
        # Decode the token from base64
        decoded_bytes = b64decode(token.encode('ascii'))
        # Convert the decoded bytes to a string
        decoded_string = decoded_bytes.decode('utf-8')
        return int(decoded_string)
    except:
        # If decoding fails, return None
        return None
    
def is_base64(s):
    try:
        # Decode the token
        decoded_bytes = b64decode(s)
        # If decoding succeeds, it's a valid base64 token
        return True
    except:
        # If decoding fails, it's not a valid base64 token
        return False