from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse, reverse_lazy
from lipila.tests.base import FunctionalTest
from django.conf import settings
from django.test import override_settings
from django.contrib.auth.hashers import make_password
from unittest.mock import Mock, patch
from accounts.models import CreatorProfile
from patron.models import WithdrawalRequest, Tier, TierSubscriptions
from django.contrib.auth import get_user_model


class CreatePatronProfileTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a super user default api-user
        self.super_user = get_user_model().objects.create_user(
            username='staff', email='test@bot.io', password='testpassword', is_superuser=True, is_staff=True)

        # create patron user
        self.user1 = get_user_model().objects.create_user(
            username='testuser', email='test3@bot.io', password='testpassword')
        self.base_url = self.live_server_url
        
    @override_settings(DEBUG=True)
    def test_create_patron_valid(self):
        """User is taken to patron profile creation page"""
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='signin']")
        login_button.click()
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, 'accounts/profile/create/creator')
        self.assertIn("Create Creator Profile", self.BROWSER.title)

        #  Create Profile
        # form = self.wait_for(By.TAG_NAME, 'form')
        patron_title = self.BROWSER.find_element(By.ID, 'id_patron_title')
        category = self.BROWSER.find_element(By.ID, 'id_creator_category')
        location = self.BROWSER.find_element(By.ID, 'id_location')
        adults_group = self.BROWSER.find_element(By.ID, 'id_adults_group')

        patron_title.send_keys('Test patron')
        category.send_keys('Artist')
        location.send_keys('Lusaka')
        adults_group.send_keys('checked')
        create_btn = self.BROWSER.find_element(
            By.CLASS_NAME, "create-btn")
        create_btn.click()

        success_msg = self.wait_for(class_name='message').text
        self.assertIn(f"Your profile data has been saved.", success_msg)
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, 'patron/accounts/profile/')


    @override_settings(DEBUG=True)
    def test_continue_has_fan(self):
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='signin']")
        login_button.click()
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, 'accounts/profile/create/creator')
        self.assertIn("Create Creator Profile", self.BROWSER.title)

        # click continue has fan link
        link = self.BROWSER.find_element(By.TAG_NAME, 'a')
        link.click()
        success_msg = self.wait_for(class_name='message').text
        self.assertIn(f"Your profile data has been saved.", success_msg)
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, '/patron/creators/list')
        self.assertIn("Browse Creators", self.BROWSER.title)

