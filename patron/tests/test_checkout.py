import requests
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from patron.models import Payment, Tier
from accounts.models import CreatorProfile



class CheckoutSupportViewAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='tetsuser@email.io', password='12345')
        self.patron = get_user_model().objects.create_user(username='testpatron', email='tetspatron@emil.io', password='12345')
        self.creator = CreatorProfile.objects.create(user=self.user, patron_title='testpatron')
        self.payee = self.creator.patron_title
        Tier().create_default_tiers(self.creator)
        self.url = reverse('checkout_support', args=[self.payee])


    @patch('lipila.views.process_mtn_payment')
    def test_valid_mtn_payment(self, mock_mtn_payment):
        # Arrange
        mock_mtn_payment.return_value.status_code = 200  # Simulating a successful MTN payment
        self.client.login(username='testpatron', password='12345')

        post_data = {
            'wallet_type': 'mtn',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'add_contribution': 'on'
        }

        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after success
        self.assertRedirects(response, reverse('subscriptions_history'))

        payment = Payment.objects.get(reference='12345ABC')
        self.assertEqual(payment.payer, self.patron.username)
        self.assertEqual(payment.amount, 52.5)  # Amount + K2.50 contribution
        self.assertEqual(payment.status, 'success')

    def test_invalid_payment_form(self):
        # Arrange
        self.client.login(username='testpatron', password='12345')

        post_data = {
            'wallet_type': '',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': self.patron
        }

        # Act
        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 200)  # Expecting the same form with errors
        self.assertContains(response, "Field errors!")  # Error message returned in context


    @patch('lipila.views.process_mtn_payment')
    def test_failed_mtn_payment(self, mock_mtn_payment):
        # Arrange
        mock_mtn_payment.return_value.status_code = 400  # Simulate failure
        self.client.login(username='testpatron', password='12345')

        post_data = {
            'wallet_type': 'mtn',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': 'testpatron'
        }

        # Act
        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertIn('Failed to initiate payment', response.json()['message'])


    @patch('requests.post')
    def test_airtel_payment_request(self, mock_post):
        # Arrange
        mock_post.return_value.status_code = 201  # Simulate Airtel API success
        mock_post.return_value.json.return_value = {'status': 'success', 'transaction_id': 'TX123'}

        self.client.login(username='testpatron', password='12345')

        post_data = {
            'wallet_type': 'airtel',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': 'testpatron@io.com'
        }

        # Act
        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')


    @patch('requests.post')
    def test_airtel_payment_failure(self, mock_post):
        # Arrange
        mock_post.return_value.status_code = 500  # Simulate Airtel API failure

        # self.client.force_login(self.patron)

        post_data = {
            'wallet_type': 'airtel',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': 'testpatron'
        }

        # Act
        response = self.client.post(self.url, post_data)
        

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['status'], 'error')
        self.assertIn('Failed to initiate payment', response.json()['message'])


class CheckoutSupportViewAnonymousTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='tetsuser@email.io', password='12345')
        self.patron = get_user_model().objects.create_user(username='testpatron', email='tetspatron@emil.io', password='12345')
        self.creator = CreatorProfile.objects.create(user=self.user, patron_title='testpatron')
        self.payee = self.creator.patron_title
        Tier().create_default_tiers(self.creator)
        self.url = reverse('checkout_support', args=[self.payee])


    @patch('lipila.views.process_mtn_payment')
    def test_valid_mtn_payment(self, mock_mtn_payment):
        # Arrange
        mock_mtn_payment.return_value.status_code = 200  # Simulating a successful MTN payment
        
        post_data = {
            'wallet_type': 'mtn',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            # 'payer': self.patron,
            'add_contribution': 'on'
        }

        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after success
        self.assertRedirects(response, reverse('accounts:signup'))

        payment = Payment.objects.get(reference='12345ABC')
        self.assertEqual(payment.payer, '260123456789')
        self.assertEqual(payment.amount, 52.5)  # Amount + K2.50 contribution
        self.assertEqual(payment.status, 'success')

    def test_invalid_payment_form(self):
        # Arrange
        
        post_data = {
            'wallet_type': '',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
        }

        # Act
        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 200)  # Expecting the same form with errors
        self.assertContains(response, "Field errors!")  # Error message returned in context


    @patch('lipila.views.process_mtn_payment')
    def test_failed_mtn_payment(self, mock_mtn_payment):
        # Arrange
        mock_mtn_payment.return_value.status_code = 400  # Simulate failure
        
        post_data = {
            'wallet_type': 'mtn',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': 'testpatron'
        }

        # Act
        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertIn('Failed to initiate payment', response.json()['message'])


    @patch('requests.post')
    def test_airtel_payment_request(self, mock_post):
        # Arrange
        mock_post.return_value.status_code = 201  # Simulate Airtel API success
        mock_post.return_value.json.return_value = {'status': 'success', 'transaction_id': 'TX123'}

        post_data = {
            'wallet_type': 'airtel',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': 'testpatron@io.com'
        }

        # Act
        response = self.client.post(self.url, post_data)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')


    @patch('requests.post')
    def test_airtel_payment_failure(self, mock_post):
        # Arrange
        mock_post.return_value.status_code = 500  # Simulate Airtel API failure
        post_data = {
            'wallet_type': 'airtel',
            'reference': '12345ABC',
            'amount': 50,
            'msisdn': '260123456789',
            'payer': 'testpatron'
        }

        # Act
        response = self.client.post(self.url, post_data)
        

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['status'], 'error')
        self.assertIn('Failed to initiate payment', response.json()['message'])


