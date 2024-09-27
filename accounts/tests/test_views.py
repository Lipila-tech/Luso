from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.contrib.auth import get_user_model
# custom modules
from accounts.models import UserSocialAuth
from accounts.utils import basic_auth_encode, basic_auth_decode
tiktok_redirect_url = settings.TIKTOK_SERVER_ENDPOINT_REDIRECT


class TikTokCallbackViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_code = 'valid_code'
        self.valid_state = 'valid_state'
        self.valid_scope = 'user.info.basic'
        self.valid_refresh_token = 'valid_refresh_token'
        self.csrf_cookie_name = 'csrfState'
        self.tiktok_token_url = 'https://www.tiktok.com/v2/tiktok_oauth/token/'
        self.tiktok_url = reverse('accounts:tiktok_callback')

        # Set up valid payload and response for mocking TikTok token exchange
        self.payload = {
            'client_key': 'fake_client_key',
            'client_secret': 'fake_client_secret',
            'code': self.valid_code,
            'grant_type': 'authorization_code',
            'redirect_uri': f'https://{tiktok_redirect_url}'
        }

    def test_missing_code_or_state_returns_bad_request(self):
        response = self.client.get(self.tiktok_url, {'state': 'some_state'})
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Server error")

    def test_invalid_csrf_state_returns_bad_request(self):
        # Simulate request with no csrfState cookie
        response = self.client.get(
            self.tiktok_url, {'code': self.valid_code, 'state': self.valid_state})
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Server error")

        # Simulate request with invalid csrfState
        self.client.cookies[self.csrf_cookie_name] = 'invalid_state'
        response = self.client.get(
            self.tiktok_url, {'code': self.valid_code, 'state': self.valid_state})
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Server error")
    
    @patch('accounts.views.TIKTOK_CLIENT_KEY', 'fake_client_key')
    @patch('accounts.views.TIKTOK_CLIENT_SECRET', 'fake_client_secret')
    @patch('accounts.views.TIKTOK_SERVER_ENDPOINT_REDIRECT', f'{tiktok_redirect_url}')
    @patch('accounts.views.py_requests.post')
    def test_valid_callback_exchanges_token(self, mock_post):
        # Simulate a valid request with correct csrfState cookie
        self.client.cookies[self.csrf_cookie_name] = self.valid_state
    
        mock_post.return_value.status_code = 200
        mock_post.return_value.headers = {
            "content-type": "application/json"}
        mock_post.return_value.json.return_value = {
            'access_token': 'act.example12345Example12345Example',
            'expires_in': 86400,
            'open_id': 'afd97af1-b87b-48b9-ac98-410aghda5344',
            'display_name': 'test_user',
            'refresh_expires_in': 31536000,
            'refresh_token': 'rft.example12345Example12345Example',
            'scope': 'user.info.basic,video.list',
            'token_type': 'Bearer'
        }

        response = self.client.get(self.tiktok_url, {
            'code': self.valid_code,
            'state': self.valid_state,
            'scope': self.valid_scope,
            'request_token': self.valid_refresh_token
        })

        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('patron/admin/profile/create_creator_profile.html')

        # Verify that the correct payload was sent in the POST request to TikTok's token URL
        mock_post.assert_called_once_with(self.tiktok_token_url, data={
            'client_key': 'fake_client_key',
            'client_secret': 'fake_client_secret',
            'code': self.valid_code,
            'grant_type': 'authorization_code',
            'redirect_uri': f'{tiktok_redirect_url}'
        })

    @patch('accounts.views.TIKTOK_CLIENT_KEY', 'fake_client_key')
    @patch('accounts.views.TIKTOK_CLIENT_SECRET', 'fake_client_secret')
    @patch('accounts.views.TIKTOK_SERVER_ENDPOINT_REDIRECT', f'{tiktok_redirect_url}')
    @patch('accounts.views.py_requests.post')
    def test_valid_callback_creates_and_authenticates_user(self, mock_post):
        # Set the csrfState cookie to match the 'state' parameter in the request
        self.client.cookies[self.csrf_cookie_name] = self.valid_state

        # Mock the response from the TikTok API
        mock_post.return_value.status_code = 200
        mock_post.return_value.headers = {"content-type": "application/json"}
        mock_post.return_value.json.return_value = {
            'access_token': 'act.example12345Example12345Example',
            'expires_in': 86400,
            'open_id': 'afd97af1-b87b-48b9-ac98-410aghda5344',
            'refresh_expires_in': 31536000,
            'username': 'test_user',
            'refresh_token': 'rft.example12345Example12345Example',
            'scope': 'user.info.basic,video.list, user.info.profile',
            'token_type': 'Bearer'
        }

        # Simulate a valid GET request to the view
        response = self.client.get(self.tiktok_url, {
            'code': self.valid_code,
            'state': self.valid_state,
            'scope': self.valid_scope,
            'request_token': self.valid_refresh_token
        })

        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('patron/admin/profile/create_creator_profile.html')

        # Verify that the user has been created in the database
        user = UserSocialAuth.objects.get(open_id='afd97af1-b87b-48b9-ac98-410aghda5344')
        self.assertIsNotNone(user)

        auth_user = get_user_model().objects.get(username='test_user')
        # Verify that the user is authenticated (logged in)
        self.assertTrue(auth_user.is_authenticated)

        # Verify that the correct payload was sent in the POST request to TikTok's token URL
        mock_post.assert_called_once_with(self.tiktok_token_url, data={
            'client_key': 'fake_client_key',
            'client_secret': 'fake_client_secret',
            'code': self.valid_code,
            'grant_type': 'authorization_code',
            'redirect_uri': f'{tiktok_redirect_url}'
        })

    def test_token_response_handling_server_error(self):
        # Simulate a valid request but TikTok's token endpoint returns a non-JSON response
        self.client.cookies[self.csrf_cookie_name] = self.valid_state

        with patch('accounts.views.py_requests.post') as mock_post:
            mock_post.return_value.status_code = 500
            mock_post.return_value.headers = {
                "content-type": "text/html"}  # Non-JSON content-type

            response = self.client.get(self.tiktok_url, {
                'code': self.valid_code,
                'state': self.valid_state,
                'scope': self.valid_scope
            })

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Server error")


class AccountsViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
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
            'email': 'newuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('accounts:signup'), data)
        # Should redirect to activation_sent view
        self.assertEqual(response.status_code, 302)

        # Check if activation email is sent
        self.assertEqual(len(mail.outbox), 1)

        # Check if user is created and not active
        new_user = get_user_model().objects.get(username='newuser')
        self.assertFalse(new_user.is_active)

        # Check if the activation email contains correct activation link
        current_site = get_current_site(response.wsgi_request)
        expected_activation_link = f'https://{current_site.domain}{reverse("accounts:activate", kwargs={"uidb64": basic_auth_encode(new_user.pk), "token": default_token_generator.make_token(new_user)})}'
        self.assertIn(expected_activation_link, mail.outbox[0].body)
