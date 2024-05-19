from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import PatronProfile, CreatorProfile


class PatronViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', password='password')

    def test_choose_profile_type(self):
        url  = "choose_profile_type"
        creator_data = {'profile_type': 'creator'}
        patron_data = {'profile_type': 'patron'}
        self.client.force_login(self.user)
        response = self.client.post(reverse(url), creator_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/create/creator")
        response = self.client.post(reverse(url), patron_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/create/patron")

    def test_redirect_unauthenticated_user(self):
        """
        Test that an unathenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/accounts/profile/")

    def test_profile_redirect(self):
        """
        Test that a user is redirected to choose a profile type
        view, if they don't have one.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/choose")

    def test_create_patron_profile(self):
        """
        Test the creation of a new user.patron_profile
        """
        self.client.force_login(self.user)
        account_number = '77477838'
        city = 'Kitwe'
        data = {'account_number': account_number, 'city': city}
        response = self.client.post(reverse('create_patron_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/")
        self.assertEqual(PatronProfile.objects.count(), 1)
        patron = PatronProfile.objects.get(user=self.user)
        self.assertEqual(patron.account_number, '77477838')
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)

    def test_create_creator_profile(self):
        """
        Test the creation of a new user.creator_profile
        """
        self.client.force_login(self.user)
        data = {
            'patron_title':'TestPatron',
            'bio':'test user bio',
            'creator_category':'artist',
        }
        response = self.client.post(reverse('create_creator_profile'), data)
        self.assertEqual(response.status_code, 302)
        print(response)
        self.assertEqual(response.url, "/accounts/profile/")
        self.assertEqual(CreatorProfile.objects.count(), 1)
        creator = CreatorProfile.objects.get(user=self.user)
        self.assertEqual(creator.patron_title, 'TestPatron')
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)
        
