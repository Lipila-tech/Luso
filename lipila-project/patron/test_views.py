from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import PatronProfile, CreatorProfile


class PatronViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_patron_profile(self):
        user = User.objects.create(username='testuser', password='password')
        self.client.force_login(user)
        account_number = '77477838'
        city = 'Kitwe'
        data = {'account_number': account_number, 'city': city}
        response = self.client.post(reverse('create_patron_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PatronProfile.objects.count(), 1)
        patron = PatronProfile.objects.get(user=user)
        self.assertEqual(patron.account_number, '77477838')

    def test_create_creator_profile(self):
        user = User.objects.create(username='testsuser', password='password')
        self.client.force_login(user)
        print('logged in')
        data = {
            'account_number':'88333',
            'bio':'test user bio',
            'city':'test city',
            'creator_category':'test category',
            'facebook_url':'test fb',
            'twitter_url':'test x',
            'instagram_url':'tets insta',
            'linkedin_url':'test lk',
        }
        print('about to post')
        response = self.client.post(reverse('create_creator_profile'), data)
        print('response is', response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CreatorProfile.objects.count(), 1)
