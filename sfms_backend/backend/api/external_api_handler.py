""" Handles MoMo API calls"""
import requests
import json
from django.http import HttpResponse

class APIHandler():
    basic = 'Basic NjM1OWNhM2EtN2M1NC00M2I3LWJlN2MtNGRjZDY1NTBmMGE2OmRjNjNjZDNmMjI4ODQwYWJiMDY0ZmY1YTdiYTUyNjNj'
    # Global authentication headers
    def __init__(self):
        self.subscription_key = '2d2aaaf890fd44828e0977303c1a0ab7'
        self.x_target_environment = 'sandbox'
        self.content_type = 'application/json'
        self.x_reference_id = ''
        self.api_key = ''
        self.api_token = 'Bearer '

    # Handle Momo
    def get_uuid(self,):
        # Get UUID
        url = "https://www.uuidgenerator.net/api/version4"
        payload={}
        headers = {}
        try:
            res = requests.get(url, headers=headers, data=payload)
            self.x_reference_id = self.x_reference_id + res.text
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        return (res)


    def create_api_user(self):
        # CREATE API USER
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"

        payload = json.dumps({
            "providerCallbackHost": "https://webhook.site/48b519d0-d2f6-479e-8f51-142aa1267a89"
        })
        headers = {
            'X-Reference-Id': self.x_reference_id,
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Content-Type': self.content_type
        }
        try:
            res = requests.request('POST', url, headers=headers, data=payload)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        return (res)

    def get_api_key(self):
        # GET API KEY
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{}/apikey".format(self.x_reference_id)

        payload={}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        try:
            res = requests.post(url, headers=headers, data=payload)
            key = res.json()
            self.api_key = self.api_key + key['apiKey']
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        return (res)

    def get_api_token(self):
        # Generate API token
        url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
     
        payload={}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Authorization': self.basic
        }
        try:
            res = requests.post(url, headers=headers, data=payload)
            token = res.json()
            self.api_token = self.api_token + token['access_token']
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        return (res)

    def request_to_pay(self, amount, partyId, externalId ):
        # Request to pay
        if len(partyId) != 10:
            raise ValueError("PartyId must be 10 digits")
        if not isinstance(amount, str):
            raise TypeError("Amount must be string")
        if not isinstance(partyId, str):
            raise TypeError("PartyId must be string")
        if not isinstance(externalId, str):
            raise TypeError("ExternalId must be string")

        url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"

        payload = json.dumps({
            "amount": amount,
            "currency": 'EUR',
            "externalId": externalId,
            "payer": {
            "partyIdType": "MSISDN",
            "partyId": partyId
            },
            "payerMessage": "Pay for Tuition",
            "payeeNote": "Termly Fees"
        })
        headers = {
            'X-Reference-Id': self.x_reference_id,
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'X-Target-Environment': self.x_target_environment,
            'Authorization': self.api_token,
            'Content-Type': self.content_type
        }

        try:
            result = requests.post(url, headers=headers, data=payload)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

        return result