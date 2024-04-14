from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse
# Assuming your models are in these files (update paths if necessary)
from business.models import BusinessUser
from creators.models import CreatorUser
from LipilaInfo.models import LipilaUser
from LipilaInfo.forms.forms import ContactForm


class LoginViewTest(TestCase):

    def setUp(self):
        # Create test users of each type (replace with your data)
        self.business_user = BusinessUser.objects.create_user(
            username='business_user', password='business_password', is_active=True)
        self.creators_user = CreatorUser.objects.create_user(
            username='creators_user', password='creators_password', is_active=True)
        self.lipila_user = LipilaUser.objects.create_user(
            username='lipila_user', password='lipila_password', is_active=True)

    def test_login_success_business_user(self):
        """Test successful login for BusinessUser and redirect to business dashboard"""
        login_data = {'username': 'business_user', 'password': 'business_password'}
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('business_dashboard'))

    def test_login_success_creators_user(self):
        """Test successful login for CreatorsUser and redirect to creators dashboard"""
        login_data = {'username': 'creators_user', 'password': 'creators_password'}
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('creators_dashboard'))

    def test_login_success_lipila_user(self):
        """Test successful login for LipilaUser and redirect to lipila dashboard"""
        login_data = {'username': 'lipila_user', 'password': 'lipila_password'}
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('lipila_dashboard'))

    def test_login_failure(self):
        """Test login failure with invalid credentials"""
        login_data = {'username': 'invalid_user', 'password': 'invalid_password'}
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)  # Expect form to render again
        self.assertContains(response, 'Your username and password didn\'t match')


class ContactViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_contact_success(self):
        """Test successful contact form submission"""
        valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message',
        }
        response = self.client.post(reverse('contact'), valid_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('index'))  # Check redirect to success page
        self.assertEqual(messages.get_messages(self.client)[0].message,  # Check success message
                         "Your message has been sent successfully")

    def test_contact_failure(self):
        """Test contact form submission with invalid data"""
        invalid_data = {'message': ''}  # Missing required fields
        response = self.client.post(reverse('contact'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Check form renders again
        self.assertContains(response, 'This field is required.')  # Check for validation error