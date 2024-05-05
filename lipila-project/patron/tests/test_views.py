from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest import mock
# Custom modules
from patron.models import CreatorUser, PatronUser
from lipila.helpers import get_user_object, check_if_user_is_patron
from lipila.forms.forms import ContactForm


class TestJoinView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_object = User.objects.create_user(
            'test_user', 'test@example.com', 'password123')
        self.creator_object = CreatorUser.objects.create_user(
            'creator_user', 'creator@example.com', 'password123')

    def test_get_not_logged_in(self):
        """Test GET request without login"""
        response = self.client.get(reverse(
            'join', kwargs={'user': self.user_object, 'creator': self.creator_object}))
        # Redirect to login page (302)
        self.assertEqual(response.status_code, 302)

    def test_get_logged_in_not_patron(self):
        """Test GET request, logged in but not a patron"""
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse(
            'join', kwargs={'user': self.user_object, 'creator': self.creator_object}))
        # Successful GET request (200)
        self.assertEqual(response.status_code, 200)
        # Check for used template
        self.assertTemplateUsed(response, 'lipila/admin/join.html')

    def test_get_logged_in_patron_not_subscribed(self):
        """Test GET request, logged in as patron but not subscribed"""
        PatronUser.objects.create(user=self.user_object)
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse(
            'join', kwargs={'user': self.user_object, 'creator': self.creator_object}))
        # Successful GET request (200)
        self.assertEqual(response.status_code, 200)
        # Check for used template
        self.assertTemplateUsed(response, 'lipila/admin/join.html')
        # Check if 'is_patron' is False
        self.assertFalse(response.context['is_patron'])

    def test_get_logged_in_patron_subscribed(self):
        """Test GET request, logged in as patron and already subscribed"""
        patron = PatronUser.objects.create(user=self.user_object)
        patron.patron.add(self.creator_object)
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse(
            'join', kwargs={'user': self.user_object, 'creator': self.creator_object}))
        # Successful GET request (200)
        self.assertEqual(response.status_code, 200)
        # Check for used template
        self.assertTemplateUsed(response, 'lipila/admin/join.html')
        # Check if 'is_patron' is True
        self.assertTrue(response.context['is_patron'])

    def test_post_not_logged_in(self):
        """Test POST request without login"""
        response = self.client.post(reverse(
            'join', kwargs={'user': self.user_object, 'creator': self.creator_object}))
        # Redirect to login page (302)
        self.assertEqual(response.status_code, 302)

    def test_post_invalid_form(self):
        """Test POST request with invalid form"""
        self.client.login(username='test_user', password='password123')
        response = self.client.post(reverse('join', kwargs={
                                    'user': self.user_object, 'creator': self.creator_object}), {'invalid_field': 'invalid_data'})
        self.assertEqual(response.status_code, 200)  # Render form again (200)
        # Check for used template
        self.assertTemplateUsed(response, 'lipila/admin/join.html')

    # Mock the check_if_user_is_patron function
    @mock.patch('lipila.helpers.check_if_user_is_patron')
    def test_post_valid_form_new_patron(self, mock_check):
        """Test POST request with valid form, creating a new PatronUser"""

        # Mock the check_if_user_is_patron function to return False (user is not a patron)
        mock_check.return_value = False

        self.client.login(username='test_user', password='password123')
        data = {'subscription': 'one'}  # Replace with actual form field names
        response = self.client.post(reverse(
            'join', kwargs={'user': self.user_object, 'creator': self.creator_object}), data)

        # Check for successful form submission and redirection
        self.assertEqual(response.status_code, 302)
        # Redirect to patron list after successful join
        self.assertEqual(response.url, reverse('patron'))
        self.assertTemplateUsed('lipila/admin/patron.html')
        # Assert that PatronUser object is created and saved
        patron = PatronUser.objects.get(user=self.user_object)
        # Check if PatronUser has a primary key (saved)
        self.assertTrue(patron.pk is not None)

        # # Assert that the creator is added to the patron's patron
        # self.assertTrue(patron.patron.filter(pk=self.creator_object.pk).exists())

        # # Verify that check_if_user_is_patron was called with expected arguments
        # mock_check.assert_called_once_with(self.user_object, self.creator_object)


class TestCheckIfUserIsPatron(TestCase):
    def setUp(self):
        # Create a User (or User) for testing
        self.user_object = User.objects.create_user(
            'test_user', 'test@example.com', 'password123')
        self.creator_object = CreatorUser.objects.create_user(
            'test_creator', 'test1@example.com', 'password123')

    def test_user_is_patron_false(self):
        # Create a PatronUser object for the user
        PatronUser.objects.create(user=self.user_object)

        is_patron = check_if_user_is_patron(
            self.user_object, self.creator_object)
        self.assertFalse(is_patron)

    def test_user_is_not_patron_no_patron_object(self):
        # User exists but doesn't have a PatronUser
        is_patron = check_if_user_is_patron(
            self.user_object, self.creator_object)
        self.assertFalse(is_patron)