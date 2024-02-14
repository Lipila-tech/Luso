
"""
Test the MTN Views
"""
from django.contrib.auth.models import User
from django.test import TestCase, Client
from api.models import LipilaPayment, MyUser

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from backend.settings import BASE_DIR

class LipilaCollectionViewTest(APITestCase):

    def test_get_payments(self):
        """Tests retrieving a list of payments."""
        url = reverse('lipila-payment-list')  # Generate URL using basename
        response = self.client.get(url)

        # Assert successful response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)  # Assert data is a list

    def test_create_payment(self):
        """Tests creating a payment with date deserialization."""
        data1 = {
            "amount": 100,
            "description": "test description",
            "payer_account": "8855994499",
            "payer_name": "test payer name",
            "payer_email": "test@bot.com",
            "receiver_account": "9988557733",
            "status": 'success',
        }
        data2 = {
            "amount": 400,
            "description": "test description",
            "payer_account": "8855994499",
            "payer_name": "test payer name",
            "payer_email": "test@bot.com",
            "receiver_account": "9988557733",
            "status": 'pending',
        }
        url = reverse('lipila-payment-list')
        response = self.client.post(url, data1)

        self.assertEqual(response.status_code, 202)  # Assert payment accepted
        # Assert successful creation
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(LipilaPayment.objects.count(), 1)
        T1 = LipilaPayment.objects.get(id=1)  # get first object
        self.assertEqual(T1.amount, 100)
        self.assertEqual(T1.status, 'success')  # assert success

        response = self.client.post(url, data2)  # make second payment
        # assert successful creation
        self.assertEqual(LipilaPayment.objects.count(), 2)
        T2 = LipilaPayment.objects.get(id=2)  # get second object
        self.assertEqual(T2.amount, 400)
        self.assertEqual(T2.payer_name, 'test payer name')
        self.assertEqual(T2.status, 'success')  # assert success
        # assert unique reference_id
        self.assertNotEqual(T1.reference_id, T2.reference_id)


class ViewsTestCaseGet(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewsTestCaseGet, cls).setUpClass()
    # def setUp(self):
        # Endpoints
        cls.payment_url = '/api/v1/payment/'
        image_file = str(BASE_DIR) + 'api/static/img/logo.png'

        cls.profile_url = '/api/v1/profile/?user=pita'
        user0 = MyUser.objects.create_user(username='pita',
                                           password='pwd_123',
                                           email='pita@example.com',
                                           profile_image=image_file)

        user1 = MyUser.objects.create_user(username='pit',
                                           password='pwd_123',
                                           email='pita@example.com',
                                           profile_image=image_file)

    # TEST GET REQUESTS

    def test_invalid_route(self):
        """ GET invalid route """
        r1 = Client().get("/api/v1/not_a_view/")
        self.assertEqual(r1.status_code, 404)

    def test_get_response_200(self):
        get_payment = Client().get(ViewsTestCaseGet.payment_url)
        get_profile = Client().get(self.profile_url)

        self.assertEqual(get_payment.status_code, 200)
        self.assertEqual(get_profile.status_code, 200)

    def test_index_200(self):
        get_index = Client().get('/api/v1/index/')
        self.assertEqual(get_index.status_code, 200)

    def test_pages_faq_200(self):
        get_faq = Client().get('/api/v1/pages-faq/')
        self.assertEqual(get_faq.status_code, 200)

    def test_dashboard_get(self):
        get_dashboard1 = Client().get('/api/v1/dashboard/?user=1&format=json')
        get_dashboard2 = Client().get('/api/v1/dashboard/?user=2&format=json')
        get_dashboard3 = Client().get('/api/v1/dashboard/?user=3&format=json')
        get_dashboard4 = Client().get('/api/v1/dashboard/?user=pit&format=json')
        self.assertEqual(get_dashboard1.status_code, 200)
        self.assertEqual(get_dashboard2.status_code, 200)
        self.assertEqual(get_dashboard3.context['status'], 404)
        self.assertTemplateUsed(get_dashboard3, 'AdminUI/pages-error.html')
        self.assertEqual(get_dashboard4.context['status'], 400)
        self.assertTemplateUsed(get_dashboard4, 'AdminUI/pages-error.html')
        self.assertEqual(get_dashboard4.context['message'], 'User ID must be of type int')   

    def test_users_profile_get(self):
        get_profile1 = Client().get('/api/v1/users-profile/?user=1&format=json')
        get_profile5 = Client().get('/api/v1/users-profile/?user=5&format=json')
        get_profile6 = Client().get('/api/v1/users-profile/?user=b&format=json')
        self.assertEqual(get_profile1.status_code, 200)
        self.assertTemplateUsed(get_profile5, 'AdminUI/pages-error.html')
        self.assertEqual(get_profile5.context['status'], 404)
        self.assertEqual(get_profile5.context['message'], 'User Profile Not Found!')
        self.assertEqual(get_profile6.context['status'], 400)
        self.assertTemplateUsed(get_profile6, 'AdminUI/pages-error.html')
        self.assertEqual(get_profile6.context['message'], 'User ID must be of type int')


class ViewsTestCasePost(TestCase):
    """Tests for the application views."""

    def setUp(self):
        # Endpoints
        self.payment_url = '/lipila/api/v1/payment/'
        self.profile_url = '/lipila/api/v1/profile/'

        # Create User objects
        self.user0 = User.objects.create_user(username='pita',
                                              password='pwd_123',
                                              email='pita@example.com')
        self.user0.save()  # save to db
        self.user1 = User.objects.create_user(username='sepi',
                                              password='pwd_123',
                                              email='sepi@example.com')
        self.user1.save()  # save to db

    # TEST AUTH
    def test_login_success(self):
        """ TEST if login was succesful"""
        login = Client().login(username='pita', password='pwd_123')
        self.assertTrue(login)

    def test_logout_success(self):
        """test if session ended successfully"""
        logout = Client().post("/lipila/api/v1/logout")
        self.assertTrue(logout)

    def test_wrong_credentials(self):
        login = Client().login(username='pitaz', password='pwd_123')
        self.assertFalse(login)
