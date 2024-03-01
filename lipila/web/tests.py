from django.test import TestCase, Client
from django.urls import reverse
from web.forms.forms import SignupForm
from django.contrib.messages import get_messages

from api.models import MyUser


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
        user = MyUser.objects.get(username='testuser')
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