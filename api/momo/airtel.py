"""Defines classes and methods that interact witht he airtel momo api"""
import requests
import json

class AirtelMomo():

    def authorization(self, client_id: str, client_secret: str) -> json:
        """
        This function is used to get OAUTH2 access_token from the api
        that will be used as bearer token for the API that we will be going calling.

        Args:
            client_id(str): string formated uuid4 number unique for all clients.
            client_secret(str): str formatted uuid4 found in airtels dashboard.

        Returns: Json object with  {access_token: "", expires_in:"", "token_type":"bearer"}
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
        }

        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        # Production -- https://openapi.airtel.africa/
        r = requests.post('https://openapiuat.airtel.africa/auth/oauth2/token', data=body, params={
        }, headers=headers)

        return r.json()


    def disburse(self, pin: str, reference: str, payee={}, transaction={}) -> json:
        """
        This function is ude to send money to a user.

        Args:
            pin(str): Encrypted four digit numeric pin to be send in 
                    a transaction request to complete the payment
            reference(str): Reference for service / goods purchased.
            payee['wallet'](str): Type of wallet where the payee wants the money to be credited.
            payee['msisdn'](str): the mobile number of the payee to pay to.
            transaction[id](str): unique random transaction id
            transaction[amount](int): the amount to collect from a consumer.
            transaction[country](str): the country of the consumer(optional)
            transaction[currency](str): the currency of the consumer(optional).

        Returns: json object.
        """

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-Country': 'ZM',
            'X-Currency': 'ZMW',
            'Authorization': 'Bearer UCcp1oe*******xCzki2w',
            'x-signature': 'MGsp*********Ag==',
            'x-key': 'DVZC*******************NM='
        }
        body = {
            "payee": {
                "msisdn": "75****26",
                "wallet_type": "SALARY or NORMAL"
            },
            "reference": "AB***141",
            "pin": "KYJ************Rsa44",
            "transaction": {
                "amount": 1000,
                "id": "AB***141",
                "type": "B2C or B2B"
            }
        }
        r = requests.post(
            'https://openapiuat.airtel.africa/standard/v3/disbursements',  params={}, headers=headers)

        return r.json()


    def request_payment(self, access_token: str, reference: str, subscriber={}, transaction={}) -> json:
        """
        This function is used to request a payment from a consumer.

        Args:
            access_token(str): OAUTH2 str from airtel used to access api
            reference(str): Reference for service / goods purchased.
            subscriber['country'](str): the country of the subscriber.
            subscriber['currency'](str): the currency of the subscriber(optional).
            subscriber['msisdn'](str): the mobile number of the subscriber to collect from.
            transaction[id](str): unique random transaction id
            transaction[amount](int): the amount to collect from a consumer.
            transaction[country](str): the country of the consumer(optional)
            transaction[currency](str): the currency of the consumer(optional).

        Returns: json object.
        """

        headers = {
            'Accept': '*/* ',
            'Content-Type': 'application/json',
            'X-Country': 'UG',
            'X-Currency': 'UGX',
            'Authorization': f'Bearer {access_token}',
            ' x-signature': 'MGsp*****************Ag==',
            ' x-key': 'DVZC*******************NM='
        }

        body = {
            "reference": reference,
            "subscriber": {
                "country": subscriber['country'],
                "currency": subscriber['currency'],
                "msisdn": subscriber['msisdn']
            },
            "transaction": {
                "amount": transaction['amount'],
                "country": transaction['country'],
                "currency": transaction['currency'],
                "id": id
            }
        }
        # Production -- https://openapi.airtel.africa/
        r = requests.post(
            'https://openapiuat.airtel.africa/merchant/v2/payments/', data=body, params={}, headers=headers)

        return r.json()


    def get_transaction_status(self, id: str, transType:str, version:int) -> json:
        """
        This function is used to enqire for the transaction status
        matching id.

        Args:
            id(str): The transaction id of a completed transaction.
            transType(str): the type of transaction. options are (payments or disbursements)
            version(int): the version of the api (payments=v1 disbursements=v3)

        Returns: str
        """
        import requests

        headers = {
            'Accept': '*/* ',
            'X-Country': 'UG',
            'X-Currency': 'UGX',
            'Authorization': 'Bearer UC*******2w'
        }
        r = requests.get(
            'https://openapiuat.airtel.africa/standard/v{version}/{transType}/{id}', headers=headers)

        return r.json()


    def call_back(self, call_back_path):
        """
        This functions checks the status of the transaction.
        Args:
            call_back_path(str): Should be set in airtel dashboard application settings.

        Returns: json object
        """
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(
            f'https://openapiuat.airtel.africa/{call_back_path}',  params={}, headers=headers)

        return r.json()


    def get_balance(self,):
        headers = {
            'Accept': '*/*',
            'X-Country': 'UG',
            'X-Currency': 'UGX',
            'Authorization': 'Bearer UC*****2w'
        }
        r = requests.get(
            'https://openapiuat.airtel.africa/standard/v1/users/balance', headers=headers)
        
        return r.json()
