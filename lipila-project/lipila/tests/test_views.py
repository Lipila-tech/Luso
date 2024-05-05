from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest import mock
# Custom modules
from business.models import BusinessUser
from patron.models import CreatorUser, PatronUser
from lipila.models import ContactInfo, HeroInfo, UserTestimonial
from lipila.helpers import get_user_object, check_if_user_is_patron
from lipila.forms.forms import ContactForm


class IndexViewTest(TestCase):
    def setUp(self):
        # Create test data (consider using @skip_unless for helper functions)
        ContactInfo.objects.create(
            street="Test Street",
            location="Test Location",
            phone1="123-456-7890",
            email1="test@example.com",
        )
        HeroInfo.objects.create(
            message="Test message",
            slogan="Test slogan",
        )
        UserTestimonial.objects.create(user=User.objects.create(username="test_user"), message="Test testimonial")

    def test_index_view_success(self):
        """Test index view renders successfully with context data"""
        url = reverse('index')  # Generate the URL for the index view
        response = self.client.get(url)

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)

        # Assert template used
        self.assertTemplateUsed(response, 'index.html')

        # Assert context data (consider using more specific assertions)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('contact', response.context)
        self.assertIn('lipila', response.context)
        self.assertIn('testimony', response.context)


class ContactFormViewTest(TestCase):

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
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(
            str(messages[0]), "Your message has been sent successfully")

    def test_contact_failure(self):
        """Test contact form submission with invalid data"""
        invalid_data = {'message': ''}  # Missing required fields
        response = self.client.post(reverse('contact'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Check form renders again
