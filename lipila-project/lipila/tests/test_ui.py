from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from django.urls import reverse, reverse_lazy
from .base import FunctionalTest
from django.contrib.auth.models import User
from django.test import override_settings
from django.contrib.auth.hashers import make_password

from accounts.models import CreatorProfile
from patron.models import WithdrawalRequest


class GetHomePageTest(FunctionalTest):
     def test_get_index(self):
        url = self.live_server_url
        self.BROWSER.get(url)
        self.assertIn('Lipila-Home', self.BROWSER.title)
        

class LoginUsersTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        self.user1 = User.objects.create_user(
            username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(
            username='testcreator', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')
        
        self.base_url = self.live_server_url

    @override_settings(DEBUG=True)
    def test_login_creator_user(self):
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testcreator')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='login']")
        login_button.click()
        self.assertIn('Lipila-Profile', self.BROWSER.title)

    @override_settings(DEBUG=True)
    def test_login_ordinary_user(self):
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='login']")
        login_button.click()
        self.assertIn('Lipila-Profile', self.BROWSER.title)


class ApproveWithdrawalTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        self.user1 = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True)
        self.user2 = User.objects.create_user(
            username='testcreator', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')
        self.withdrawal_request = WithdrawalRequest.objects.create(
            creator=self.creator_user,
            amount=100.00,
            account_number='0966445333',
        )
        self.base_url = self.live_server_url
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='login']")
        login_button.click()
    

    @override_settings(DEBUG=True)
    def test_approve_withdraw_modal_cancel_btn(self):
        url = f'{self.base_url}/approve_withdrawals/'
        self.BROWSER.get(url)

        self.assertIn('Pending Withdrawals', self.BROWSER.title)
        header_text = self.BROWSER.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Approve Withdrawal Requests', header_text)

        # User clicks the approve button
        self.BROWSER.find_element(By.CLASS_NAME, 'approve-request').click()
        
        # Confirmation modal opens
        modal = self.wait_for(element_id='confirmationModal')
        self.BROWSER.find_element(By.ID, 'cancel').click()
               
        

class RejectWithdrawalTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        self.user1 = User.objects.create_user(
            username='testuser', password='testpassword', is_staff=True)
        self.user2 = User.objects.create_user(
            username='testcreator', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')
        self.withdrawal_request = WithdrawalRequest.objects.create(
            creator=self.creator_user,
            amount=100.00,
            account_number='0966445333',
        )
        self.base_url = self.live_server_url
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='login']")
        login_button.click()
            

    @override_settings(DEBUG=True)
    def test_reject_withdraw_modal_cnacel_btn(self):
        url = f'{self.base_url}/approve_withdrawals/'
        self.BROWSER.get(url)

        self.assertIn('Pending Withdrawals', self.BROWSER.title)
        header_text = self.BROWSER.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Approve Withdrawal Requests', header_text)

        # User clicks the approve button
        self.BROWSER.find_element(By.CLASS_NAME, 'reject-request').click()
        modal = self.wait_for(element_id='confirmationModal')
        self.BROWSER.find_element(By.ID, 'cancel').click()