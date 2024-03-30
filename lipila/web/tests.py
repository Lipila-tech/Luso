from django.test import TestCase, Client
from django.urls import reverse
from web.forms.forms import SignupForm
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser  # For anonymous user test
from api.models import LipilaUser
from .helpers import set_context

# TEST SignupView
class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SignupForm)
        self.assertTemplateUsed(response, 'Auth/signup.html')

    def test_post_valid_form(self):
        data = {
            "username": "testuser",
            "phone_number": "2244556677",
            "password": "test@123",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].level, 25)
        self.assertEqual(messages[0].message, 'Account created successfully')

        # check that a user with a specified username is created
        # but not active
        user = LipilaUser.objects.get(username='testuser')
        self.assertTrue(user.is_active)

    def test_post_invalid_form(self):
        data = {
            "username": "####",
            "email": "testemail@bot.com",
            "password": "test@123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SignupForm)
        self.assertTemplateUsed(response, 'Auth/signup.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].level, 40)
        self.assertEqual(messages[0].message, 'Error during signup!')


class SetContextTests(TestCase):

    def test_valid_user(self):
        # Create a test user
        user = LipilaUser.objects.create_user(username='testuser', password='password123')

        # Call the function with the user
        context = set_context(None, user)

        # Assert expected context
        self.assertEqual(context['status'], 200)
        self.assertEqual(context['user'], user)

    def test_missing_user(self):
        # Call the function without a user
        context = set_context(None, None)

        # Assert expected error handling
        self.assertEqual(context['status'], 400)
        self.assertEqual(context['message'], 'Error, User argument missing')

    def test_invalid_user_type(self):
        # Pass an invalid user type (string instead of LipilaUser object)
        invalid_user = 'invalid_username'

        # Call the function with the invalid user
        with self.assertRaises(ValueError):
            set_context(None, invalid_user)

    def test_user_not_found(self):
        # Try to get a non-existent user
        nonexistent_username = 'nonexistentuser'

        # Call the function with the nonexistent username
        context = set_context(None, nonexistent_username)

        # Assert expected error handling
        self.assertEqual(context['status'], 404)
        self.assertEqual(context['message'], 'User Not Found!')

    def test_anonymous_user(self):
        # Use an anonymous user
        anonymous_user = AnonymousUser()

        # Call the function with the anonymous user
        context = set_context(None, anonymous_user)

        # Assert expected error handling (similar to missing user)
        self.assertEqual(context['status'], 400)
        self.assertEqual(context['message'], 'Error, User argument missing')