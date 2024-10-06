# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from api.models import MomoColTransaction
from api.momo.airtel import AirtelMomo


class AirtelTransactionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.payment_url = reverse('airtel-request-payment')
        self.callback_url = reverse('airtel-callback')
        self.valid_payload = {
            'reference': 'REF123',
            'transaction_id': 'TRANS123',
            'msisdn': '260978123456',
            'amount': 100.00
        }
    
    @patch.object(AirtelMomo, 'request_payment')  # Mocking AirtelMomo API call
    def test_initiate_payment_success(self, mock_request_payment):
        # Mocking Airtel API response
        mock_request_payment.return_value = {
            'status': 'success'
        }

        response = self.client.post(self.payment_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MomoColTransaction.objects.count(), 1)
        transaction = MomoColTransaction.objects.get()
        self.assertEqual(transaction.reference, self.valid_payload['reference'])
        self.assertEqual(transaction.msisdn, self.valid_payload['msisdn'])
        self.assertEqual(transaction.amount, self.valid_payload['amount'])
        self.assertEqual(transaction.status, 'pending')

    @patch.object(AirtelMomo, 'request_payment')  # Mocking AirtelMomo API call
    def test_initiate_payment_failure(self, mock_request_payment):
        # Mocking Airtel API failure response
        mock_request_payment.return_value = {
            'status': 'failed'
        }

        response = self.client.post(self.payment_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MomoColTransaction.objects.count(), 0)  # No transaction created

    def test_initiate_payment_invalid_data(self):
        # Send invalid payload (missing msisdn)
        invalid_payload = {
            'reference': 'REF123',
            'amount': 100.00
        }
        response = self.client.post(self.payment_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MomoColTransaction.objects.count(), 0)

    def test_callback_update_transaction_status(self):
        # Create a pending transaction in the DB
        transaction = MomoColTransaction.objects.create(
            reference='REF123',
            transaction_id='TRANS123',
            msisdn='260978123456',
            amount=100.00,
            status='pending'
        )

        # Callback payload from Airtel
        callback_payload = {
            'transaction_id': 'TRANS123',
            'status': 'completed'
        }
        response = self.client.post(self.callback_url, callback_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the transaction status is updated
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'completed')

    def test_callback_transaction_not_found(self):
        # Callback payload with a transaction ID that doesn't exist in the database
        callback_payload = {
            'transaction_id': 'INVALID123',  # Transaction ID that doesn't exist
            'status': 'completed'
        }

        # Send the callback request
        response = self.client.post(self.callback_url, callback_payload, format='json')

        # Assert that the response returns a 404 status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Also check the message returned in the response
        self.assertEqual(response.data['error'], 'Transaction not found')

