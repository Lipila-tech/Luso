import os
from django.contrib.auth.models import User
from django.test import TestCase, Client
from api.models import BusinessUser
from django.urls.exceptions import NoReverseMatch
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RedirectToLipilaTest(APITestCase):
    def test_redirect_no_user(self):
        username = 'test_user'
        url = reverse('lipila_profile', kwargs={'username': username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   
    def test_redirect_with_user_created(self):
        image_file = str(BASE_DIR) + 'api/static/img/logo.png'
        user = BusinessUser.objects.create_user(username='test_user',
                                           password='pwd_123',
                                           email='pita@example.com',
                                           profile_image=image_file)
        username = 'test_user'
        url = reverse('lipila_profile', kwargs={'username': username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, f"http://localhost:8000/profile/?username={username}")


class ViewsTestCaseGet(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewsTestCaseGet, cls).setUpClass()
    # def setUp(self):
        # Endpoints
        cls.payment_url = '/api/v1/payment/'
        image_file = str(BASE_DIR) + 'api/static/img/logo.png'

        cls.profile_url = '/api/v1/profile/?user=pita'
        user0 = BusinessUser.objects.create_user(username='pita',
                                           password='pwd_123',
                                           email='pita@example.com',
                                           profile_image=image_file)

        user1 = BusinessUser.objects.create_user(username='pit',
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
        get_dashboard2 = Client().get('/api/v1/dashboard/?user=1&format=json')
        self.assertEqual(get_dashboard1.status_code, 200)
        self.assertEqual(get_dashboard2.status_code, 200)
        

    def test_users_profile_get(self):
        get_profile1 = Client().get('/api/v1/users-profile/?user=1&format=json')
        self.assertEqual(get_profile1.status_code, 200)
        
    def test_apology_function(self):
        # Test dashboard endpoint
        get_dashboard3 = Client().get('/api/v1/dashboard/?user=3&format=json')
        get_dashboard4 = Client().get('/api/v1/dashboard/?user=pit&format=json')
        get_dashboard5 = Client().get('/api/v1/dashboard/')
        self.assertEqual(get_dashboard3.context['status'], 404)
        self.assertTemplateUsed(get_dashboard3, 'AdminUI/pages-error.html')
        self.assertEqual(get_dashboard4.context['status'], 400)
        self.assertTemplateUsed(get_dashboard4, 'AdminUI/pages-error.html')        
        self.assertEqual(get_dashboard4.context['message'], 'User ID must be of type int')
        self.assertEqual(get_dashboard5.context['status'], 400)
        self.assertTemplateUsed(get_dashboard5, 'AdminUI/pages-error.html')
        self.assertEqual(get_dashboard5.context['message'], 'Error, User argument missing')

        # Test users-profile endpoint
        get_profile5 = Client().get('/api/v1/users-profile/?user=5&format=json')
        get_profile6 = Client().get('/api/v1/users-profile/?user=b&format=json')

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
