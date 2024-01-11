""" Handles MoMo API calls"""
import requests
import json
from django.http import HttpResponseBadRequest
from django import http
from rest_framework.response import Response
from rest_framework import status
from .helpers import get_uuid4, basic_auth

import environ

env = environ.Env()

environ.Env.read_env()


class MtnApiHandler():

    def __init__(self):
        self.subscription_col_key = env("MTN_MOMO_COLLECTIONS_KEY")
        self.subscription_dis_key = env("MTN_MOMO_DISBURSEMENT_KEY")
        self.x_target_environment = env("TARGET_ENV")
        self.content_type = 'application/json'
        self.x_reference_id = get_uuid4()
        self.api_key = ''
        self.api_token = 'Bearer '

    def create_api_user(self):
        """
        Used to create an API user in the sandbox target environment.
            X-Reference-Id(string) Format - UUID V4.
            Recource ID for the API user to be created.
        """
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"

        payload = json.dumps({
            "providerCallbackHost": "{}".format(env("PROVIDER_CALLBACK_HOST"))
        })
        headers = {
            'X-Reference-Id': self.x_reference_id,
            'Ocp-Apim-Subscription-Key': self.subscription_col_key,
            'Content-Type': self.content_type
        }
        try:
            res = requests.request('POST', url, headers=headers, data=payload)
            return res
        except requests.exceptions.HTTPError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.ConnectionError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except requests.exceptions.Timeout:
            return Response(status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_api_key(self):
        """
        Used to create an API key for an API user in the sandbox target environment.
        X-Reference-Id(string) Format - UUID V4.
            Recource ID for the API user to be created.
        Ocp-Apim-Subscription-Key(string)Subscription key which provides access to this API.
        Found in your momo Profile.
        """
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{}/apikey".format(
            self.x_reference_id)

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_col_key,
        }
        try:
            res = requests.post(url, headers=headers, data=payload)
            if res.status_code == 403:
                return res
            key = res.json()
            self.api_key = self.api_key + key['apiKey']
            return res

        except requests.exceptions.HTTPError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.ConnectionError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except requests.exceptions.Timeout:
            return Response(status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_api_token(self):
        """
        This operation is used to create an access token which can then
        be used to authorize and authenticate towards the other end-points
        of the API.
        """
        url = "https://sandbox.momodeveloper.mtn.com/collection/token/"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_col_key,
            'Authorization': basic_auth(self.x_reference_id, self.api_key)
        }
        try:
            res = requests.post(url, headers=headers, data=payload)
            if res.status_code == 403:
                return res
            token = res.json()
            self.api_token = self.api_token + token['access_token']
            return res
        except requests.exceptions.HTTPError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.ConnectionError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except requests.exceptions.Timeout:
            return Response(status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def request_to_pay(self, amount, mobile, reference):
        """ Request to pay"""
        if len(mobile) != 10 or int(amount) < 10:
            raise ValueError(
                "PartyId must be 10 digits and Amount value should be greater than 10")

        if not isinstance(amount, str):
            raise TypeError("Amount must be string great than 10")
        if not isinstance(mobile, str):
            raise TypeError("PartyId must be string with 10 digits")
        if not isinstance(reference, str):
            raise TypeError("ExternalId must be string")

        try:
            url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"

            payload = json.dumps({
                "amount": amount,
                "currency": 'EUR',
                "externalId": reference,
                "payer": {
                    "partyIdType": "MSISDN",
                    "partyId": mobile
                },
                "payerMessage": "Make a donation to wicare",
                "payeeNote": "wicare donation"
            })
            headers = {
                'X-Reference-Id': self.x_reference_id,
                'Ocp-Apim-Subscription-Key': self.subscription_col_key,
                'X-Target-Environment': self.x_target_environment,
                'Authorization': self.api_token,
                'Content-Type': self.content_type
            }
            response = requests.post(url, headers=headers, data=payload)
            return response
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
