""" Handles MoMo API calls"""
import requests
import json
from rest_framework.response import Response
from ..helpers import get_uuid4, basic_auth, is_payment_details_valid

import environ

env = environ.Env()

environ.Env.read_env()


class MTNBase():
    """Base class for the mtn api"""

    def __init__(self):
        self.x_target_environment = env("TARGET_ENV")
        self.content_type = 'application/json'
        self.x_reference_id = get_uuid4()
        self.api_key = ''
        self.api_token = 'Bearer '

    def create_api_user(self, subscription_key: str):
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
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': self.content_type
        }
        try:
            response = requests.request(
                'POST', url, headers=headers, data=payload)
            if response.status_code == 201:
                return response
            elif response.status_code == 400:
                raise ValueError("Bad request")
            elif response.status_code == 409:
                raise ValueError("Conflict user exists")
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def create_api_key(self, subscription_key: str):
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
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 201:
                key = response.json()
                self.api_key = self.api_key + key['apiKey']
                return response
            elif response.status_code == 400:
                raise ValueError("Bad request")
            elif response.status_code == 404:
                raise ValueError("Not found")
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def provision_sandbox(self, subscription_key: str):
        """ creates the api user and api token
        """
        try:
            api_user = self.create_api_user(subscription_key)
            api_key = self.create_api_key(subscription_key)

            if api_user.status_code == 201 and api_key.status_code == 201:
                return api_user
            else:
                raise ValueError("Failed")
        except ValueError:
            return Response(status=api_user.status_code)

    def create_api_token(self, subscription_key: str, endpoint: str):
        """
        This operation is used to create an access token which can then
        be used to authorize and authenticate towards the other end-points
        of the API.
        requires api key
        """
        url = f"https://sandbox.momodeveloper.mtn.com/{endpoint}/token/"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Authorization': basic_auth(self.x_reference_id, self.api_key)
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                token = response.json()
                self.api_token = self.api_token + token['access_token']
                return response
            elif response.status_code == 401:
                raise ValueError("Unauthorized")
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def validate_account_holder(
            self, subscription_key: str,
            accountHolderIdType: str,
            accountHolderId: str,
            endpoint: str
    ):
        ''' checks is a payee account exists
        200 OK, 409 conflict, 400 Bad Request
        requires api token
        '''
        url = f"https://sandbox.momodeveloper.mtn.com/{endpoint}/v1_0/accountholder/{accountHolderIdType}/{accountHolderId}/active"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Authorization': self.api_token,
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise ValueError("Bad request")
            else:
                return response
        except Exception as e:
            return Response(status=response.status_code)


class Collections(MTNBase):
    """
    Handles the collections endpoint requests
    """

    def __init__(self):
        super().__init__()
        self.subscription_col_key = env("MTN_MOMO_COLLECTIONS_KEY")

    def request_to_pay(self, amount: str, payer: str, reference_id: str)->Response:
        """
        This method queries the MTN momo request to pay endpoint.

        Args:
            amount(str): The amount to collect from the payer.
            payer(str): The mtn momo registered mobile number.
            reference_id(str): Unique str formated uuid number to that identitifies the tr
                        transaction.

        Returns:
            A HTTP Response.
        """
        is_valid = is_payment_details_valid(amount, payer, reference_id)
        if is_valid:
            """ Query the Collections API"""
            try:
                url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
                payload = json.dumps({
                    "amount": amount,
                    "currency": 'EUR',
                    "externalId": reference_id,
                    "payer": {
                        "partyIdType": "MSISDN",
                        "partyId": payer
                    },
                    "payerMessage": f"send money to {payer}",
                    "payeeNote": "Lipila gateway"
                })
                headers = {
                    'X-Reference-Id': self.x_reference_id,
                    'Ocp-Apim-Subscription-Key': self.subscription_col_key,
                    'X-Target-Environment': self.x_target_environment,
                    'Authorization': self.api_token,
                    'Content-Type': self.content_type
                }
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code == 202:
                    return Response(status=202, data={'message':'pending'})
                elif response.status_code == 400:
                    return Response(status=400, data={'reason':'Bad Request'})
                elif response.status_code == 409:
                    return Response(status=409, data={'reason':'Conflict user exists'})
                elif response.status_code == 500:
                    return Response(status=500, data={'reason':'mtn server error'})
            except Exception as e:
                return Response(status=500, data={'reason':'mtn server error'})

    def get_payment_status(self, reference_id) -> Response:
        ''' checks status of payment SUCCESS or FAILED
        200 SUCCESS/FAIL, 404 not Found, 400 Bad Request
        '''
        url = "https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment/{}".format(
            reference_id)
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Ocp-Apim-Subscription-Key': self.subscription_col_key,
            'Authorization': self.api_token
        }
        try:
            response = requests.get(url, headers=headers, data={})
            if response.status_code == 200:
                return response
            elif response.status_code == 400:
                return Response(status=400, data={'reason':'Bad Request'})
            elif response.status_code == 404:
                return Response(status=404, data={'reason':'Not Found'})
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)


class Disbursement(MTNBase):
    """
    Handles the disbursement endpoint requests
    """

    def __init__(self):
        super().__init__()
        self.subscription_dis_key = env("MTN_MOMO_DISBURSEMENT_KEY")

    def deposit(self, amount: str, payer: str, reference_id: str):
        is_valid = is_payment_details_valid(amount, payer, reference_id)
        if is_valid:
            """ deposit funds to multiple users"""
            try:
                url = "https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/deposit"
                payload = json.dumps({
                    "amount": amount,
                    "currency": 'EUR',
                    "externalId": reference_id,
                    "payee": {
                        "partyIdType": "MSISDN",
                        "partyId": payer
                    },
                    "payerMessage": f"send money to {payer}",
                    "payeeNote": "Lipila gateway"
                })
                headers = {
                    'X-Reference-Id': self.x_reference_id,
                    'Ocp-Apim-Subscription-Key': self.subscription_dis_key,
                    'X-Target-Environment': self.x_target_environment,
                    'Authorization': self.api_token,
                    'Content-Type': self.content_type
                }
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code == 202:
                    return response
                elif response.status_code == 400:
                    return Response(status=400, data={'reason':'Bad Request'})
                elif response.status_code == 409:
                    return Response(status=409, data={'reason':'Conflict user exists'})
                elif response.status_code == 500:
                    return Response(status=500, data={'reason':'mtn server error'})
            except Exception as e:
                return Response(status=500, data={'reason':'mtn server error'})

    def get_transaction_status(self, transaction: str, referenceid: str):
        ''' checks status of deposit or deposit SUCCESS or FAILED
        200 SUCCESS/FAIL, 404 nOT Found, 400 Bad Request
        '''
        url = f"https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/{transaction}/{referenceid}"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Ocp-Apim-Subscription-Key': self.subscription_dis_key,
            'Authorization': self.api_token
        }
        try:
            response = requests.get(url, headers=headers, data={})
            if response.status_code == 200:
                return response
            elif response.status_code == 400:
                return Response(status=400, data={'reason':'Bad Request'})
            elif response.status_code == 404:
                return Response(status=404, data={'reason':'Not Found'})
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def get_account_balance(self):
        ''' check own account balance
        200 SUCCESS/FAIL, 404 nOT Found, 400 Bad Request
        '''
        url = f"https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/account/balance"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Ocp-Apim-Subscription-Key': self.subscription_dis_key,
            'Authorization': self.api_token
        }
        try:
            response = requests.get(url, headers=headers, data={})
            if response.status_code == 200:
                """ 
                    {
                        "availableBalance": "string",
                        "currency": "string"
                    }
                """
                return response
            elif response.status_code == 400:
                return Response(status=400, data={'reason':'Bad Request'})
            elif response.status_code == 404:
                return Response(status=404, data={'reason':'Not Found'})
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)
