import os
from django.contrib.auth.models import User
from api.models import LipilaCollection, LipilaDisbursement
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from uuid import UUID
from api.utils import generate_reference_id
from lipila.utils import check_payment_status


class LipilaDisbursementViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create(username='testuser')
        cls.url = reverse('disburse-list')
    
    
    def test_make_deposit_success(self):        
        data = {'amount': '100', 'payee_account_number': '0966443322',
                'network_operator': 'mtn', 'description': 'testdescription'}

        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(LipilaDisbursement.objects.count(), 1)
        self.assertEqual(LipilaDisbursement.objects.get().status, 'success')
        self.assertEqual(LipilaDisbursement.objects.get().api_user.username, 'testuser')
        # Attempt to convert the response to a UUID object
        try:
            # Attempt to convert the response to a UUID object
            UUID(LipilaDisbursement.objects.get().reference_id)
            self.assertTrue(True)  # Test passes if conversion is successful
        except ValueError:
            self.fail("generate_reference_id did not return a valid UUID string.")

    def test_deposit_lipila_fail_validation(self):
        data = {'amount': '100', 'payee_account_number': 'invalid',
                'network_operator': 'mtn', 'description': 'testdescription'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LipilaDisbursement.objects.count(), 0)

    def test_deposit_no_user_fail_payer(self):
        User.objects.all().delete()
        data = {'amount': '100', 'payee_account_number': '0966443322',
                'network_operator': 'mtn', 'description': 'testdescription'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LipilaDisbursement.objects.count(), 0)

    def test_get_disbursed_success(self):
        LipilaDisbursement.objects.create(
            api_user=self.user, amount=100, status='success')
        response = self.client.get(self.url, {'api_user': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_fail_no_payee(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_fail_payee_not_found(self):
        response = self.client.get(self.url, {'api_user': 'not_a_user'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LipilaCollectionViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ref = generate_reference_id()
        cls.user = User.objects.create(username='test_user1')
        cls.url = reverse('payments-list')
        
    def test_create_payment_success(self):
        data = {'amount': '100', 'payer_account_number': '0966443322',
                'network_operator': 'mtn', 'description': 'testdescription'}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(LipilaCollection.objects.count(), 1)
        self.assertEqual(LipilaCollection.objects.get().status, 'success')
        self.assertEqual(LipilaCollection.objects.get().api_user.username, 'test_user1')
        # Attempt to convert the response to a UUID object
        try:
            # Attempt to convert the response to a UUID object
            UUID(LipilaCollection.objects.get().reference_id)
            self.assertTrue(True)  # Test passes if conversion is successful
        except ValueError:
            self.fail("generate_reference_id did not return a valid UUID string.")

    def test_create_lipila_fail_validation(self):
        data = {'payer': 'lipila', 'amount': 'invalid'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LipilaCollection.objects.count(), 0)

    def test_create_nonlipila_fail_payer(self):
        data = {'amount': 100, 'payer': '0809123456'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LipilaCollection.objects.count(), 0)

    def test_get_payments_success(self):
        LipilaCollection.objects.create(
            api_user=self.user, amount=100, status='success')
        response = self.client.get(self.url, {'api_user': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_fail_no_payee(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_fail_payee_not_found(self):
        response = self.client.get(self.url, {'api_user': 'not_a_user'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
