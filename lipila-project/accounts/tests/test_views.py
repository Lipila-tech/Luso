from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.contrib import messages
# custom modules
from accounts.helpers import basic_auth_encode, basic_auth_decode


class AccountsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')

    
    def test_activation_sent_view(self):
        response = self.client.get(reverse('accounts:activation_sent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/activation_sent.html')

    def test_activate_valid_token(self):
        token = default_token_generator.make_token(self.user)
        uid64 = basic_auth_encode(self.user.pk)
        response = self.client.get(reverse('accounts:activate', kwargs={
                                   'uidb64': uid64, 'token': token}))
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_invalid_token(self):
        response = self.client.get(reverse('accounts:activate', kwargs={
                                   'uidb64': 'invalid_uid', 'token': 'invalid_token'}))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_view_post(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('accounts:signup'), data)
        # Should redirect to activation_sent view
        self.assertEqual(response.status_code, 302)

        # Check if activation email is sent
        self.assertEqual(len(mail.outbox), 1)

        # Check if user is created and not active
        new_user = User.objects.get(username='newuser')
        self.assertFalse(new_user.is_active)

        # Check if the activation email contains correct activation link
        current_site = get_current_site(response.wsgi_request)
        expected_activation_link = f'http://{current_site.domain}{reverse("accounts:activate", kwargs={"uidb64": basic_auth_encode(new_user.pk), "token": default_token_generator.make_token(new_user)})}'
        self.assertIn(expected_activation_link, mail.outbox[0].body)