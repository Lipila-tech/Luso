from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from unittest.mock import patch
from unittest.mock import Mock
# custom modules
from api.models import LipilaCollection, LipilaDisbursement
from lipila.models import (
    ContactInfo, HeroInfo, CustomerMessage, UserTestimonial)
from lipila.helpers import (
    get_lipila_contact_info,
    get_user_emails,
    get_lipila_index_page_info,
    get_testimonials,
    get_user_object,
    query_disbursement,
    query_collection,
    check_payment_status,
)
from patron.helpers import generate_reference_id

class TestCheckPaymentStatus(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin')
        self.ref1 =  generate_reference_id()
        self.ref2 =  generate_reference_id()
        self.ref3 =  generate_reference_id()
        self.payment1 = LipilaCollection.objects.create(
            api_user=self.user, amount=100, status='pending', reference_id=self.ref1)
        
        self.payment2 = LipilaDisbursement.objects.create(
            api_user=self.user, amount=101, status='success', reference_id=self.ref2)
        
    def test_collection_valid(self):
        status = check_payment_status(self.ref1, 'col')
        self.assertEqual(status, 'pending')

    def test_disbursement_valid(self):
        status = check_payment_status(self.ref2, 'dis')
        self.assertEqual(status, 'success')

    def test_collection_not_found(self):
        status = check_payment_status(self.ref3, 'col')
        self.assertEqual(status, 'transaction id not found')
    
    def test_collection_invalid_argument_option(self):
        status = check_payment_status(self.ref1, 'payment')
        self.assertEqual(status, None)

@patch('lipila.helpers.requests.get')
class GetPaymentTest(TestCase):
    def test_get_query_disbursement_valid(self, mock_get):
        User.objects.create(username='test_user')
        # Mock the response object to return expected data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Call the function with a user
        user = 'test_user'
        response = query_collection(user, 'GET')

        # Assert that the mocked function was called with the correct URL and params
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/v1/payments/",
            params={'api_user': user}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    def test_get_query_disbursement_api_user_not_found(self, mock_get):
        # Mock the response object to return expected data
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error':'api user not found'}
        mock_get.return_value = mock_response

        # Call the function with a user
        user = 'test_user'
        response = query_collection(user, 'GET')

        # Assert that the mocked function was called with the correct URL and params
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/v1/payments/",
            params={'api_user': user}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error':'api user not found'})

    def test_get_query_disbursement_invalid(self, mock_get):       
        response = query_collection('test_user', 'update')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'data':'Invalid method passed'})


@patch('lipila.helpers.requests.post')
class PostPaymentTest(TestCase):
    def test_post_query_disbursement_valid(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response

        User.objects.create(username='test_user')

        data = {'amount': '100', 'payer_account_number': '0966443322',
                'payment_method': 'mtn', 'description': 'testdescription'}
        
        response = query_collection('test_user', 'POST', data=data)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data, {'data': 'request accepted, wait for client approval'})

@patch('lipila.helpers.requests.get')
class GetDisbursementTest(TestCase):
    def test_get_query_disbursement_valid(self, mock_get):
        User.objects.create(username='test_user')
        # Mock the response object to return expected data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Call the function with a user
        user = 'test_user'
        response = query_disbursement(user, 'GET')

        # Assert that the mocked function was called with the correct URL and params
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/v1/disburse/",
            params={'api_user': user}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    def test_get_query_disbursement_api_user_not_found(self, mock_get):
        # Mock the response object to return expected data
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error':'api user not found'}
        mock_get.return_value = mock_response

        # Call the function with a user
        user = 'test_user'
        response = query_disbursement(user, 'GET')

        # Assert that the mocked function was called with the correct URL and params
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/v1/disburse/",
            params={'api_user': user}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error':'api user not found'})

    def test_get_query_disbursement_invalid(self, mock_get):       
        response = query_disbursement('test_user', 'update')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'data':'Invalid method passed'})


@patch('lipila.helpers.requests.post')
class PostDisbursementTest(TestCase):
    def test_post_query_disbursement_valid(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response

        User.objects.create(username='test_user')

        data = {'amount': '100', 'payee_account_number': '0966443322',
                'payment_method': 'mtn', 'description': 'testdescription'}
        
        response = query_disbursement('test_user', 'POST', data=data)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data, {'data': 'request accepted, wait for client approval'})
        

class HelperFunctionTests(TestCase):
    def test_get_user_object_invalid(self):
        """Test get_user_object returns None"""
        user = 'testuser'
        user_object = get_user_object(user)
        self.assertEqual(user_object, None)

    def test_get_user_object_valid(self):
        """Test get_user_object returns a User object"""
        user = User.objects.create_user('testuser', 'user@email.com', 'testpasss')
        user_object = get_user_object(user)
        self.assertTrue(isinstance(user_object, User))

    def test_get_lipila_contact_info_success(self):
        """Test get_lipila_contact_info returns contact info"""
        ContactInfo.objects.create(
            street="Test Street",
            location="Test Location",
            phone1="123-456-7890",
            email1="test@example.com",
        )
        context = get_lipila_contact_info()
        self.assertIn('contact', context)
        self.assertIsInstance(context['contact'], ContactInfo)

    def test_get_lipila_contact_info_no_data(self):
        """Test get_lipila_contact_info with no ContactInfo"""
        context = get_lipila_contact_info()
        self.assertEqual(context, {'contact': ''})

    def test_get_user_emails(self):
        """Test get_user_emails returns all user emails"""
        CustomerMessage.objects.create(
            name="Test User",
            email="test@user.com",
            subject="Test subject",
            message="Test message",
        )
        context = get_user_emails()
        self.assertIn('user_messages', context)
        self.assertIsInstance(context['user_messages'], models.QuerySet)
        # Test data has 1 email
        self.assertEqual(context['user_messages'].count(), 1)


    def test_get_lipila_index_page_info_success(self):
        """Test get_lipila_index_page_info returns indexpage info"""
        HeroInfo.objects.create(
            message="Test message",
            slogan="Test slogan",
        )  
        context = get_lipila_index_page_info()
        self.assertIn('lipila', context)
        self.assertIsInstance(context['lipila'], HeroInfo)
        self.assertEqual(context['lipila'].message, 'Test message')
        self.assertEqual(context['lipila'].slogan, 'Test slogan')

    def test_get_lipila_index_page_info_no_data(self):
        """Test get_lipila_index_page_info with no HeroInfo"""        
        context = get_lipila_index_page_info()
        self.assertEqual(context, {'lipila': ''})

    def test_get_testimonials(self):
        """Test get_testimonials returns all testimonials"""
        lipila_user = User.objects.create(username="test_user", password="test_password")
        UserTestimonial.objects.create(user=lipila_user
                                   ,message="Test testimonial",
        )
        context = get_testimonials()
        self.assertIn('testimonials', context)
        self.assertIsInstance(context['testimonials'], models.QuerySet)
        # Test data has 1 testimonial
        self.assertEqual(context['testimonials'].count(), 1)
