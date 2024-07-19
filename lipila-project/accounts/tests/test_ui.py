from selenium.webdriver.common.by import By
from django.urls import reverse
from lipila.tests.base import FunctionalTest
from django.conf import settings
from django.test import override_settings
from unittest.mock import Mock, patch
from accounts.models import CreatorProfile
from django.contrib.auth import get_user_model


class SignupTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        self.base_url = self.live_server_url

    @override_settings(DEBUG=True)
    def test_default_backend_signup_user_valid(self):
        self.BROWSER.get(f'{self.base_url}/accounts/signup/')
        email_field = self.BROWSER.find_element(By.ID, 'id_email')
        password1_field = self.BROWSER.find_element(By.ID, 'id_password1')
        password2_field = self.BROWSER.find_element(By.ID, 'id_password2')
        email_field.send_keys('testuser')
        password1_field.send_keys('testpassword')
        password2_field.send_keys('testpassword')
        signup_btn = self.BROWSER.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        signup_btn.click()
        # User sees success message after page redirection
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, 'accounts/sent/')
        self.assertEqual("Activation sent", self.BROWSER.title)


class AuthenticateUsersTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        self.user1 = get_user_model().objects.create_user(
            username='testuser', password='testpassword')
        self.user2 = get_user_model().objects.create_user(
            username='testcreator', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')

        self.base_url = self.live_server_url

    @override_settings(DEBUG=True)
    def test_default_backend_login_creator_user_valid(self):
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testcreator')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='accounts:signin']")
        login_button.click()
        self.assertIn('Lipila-Profile', self.BROWSER.title)

    @override_settings(DEBUG=True)
    def test_default_backend_login_ordinary_user_valid(self):
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='accounts:signin']")
        login_button.click()
        self.assertIn('Lipila-Profile', self.BROWSER.title)

    @override_settings(DEBUG=True)
    def test_google_sign_in_valid(self):
        self.BROWSER.get(f'{self.base_url}/accounts/login/')


