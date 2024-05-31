from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from accounts.models import PatronProfile, CreatorProfile
from patron.models import Tier


class PatronViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser', password='password')

    def test_choose_profile_type(self):
        url = "choose_profile_type"
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
        self.assertEqual(
            response.url, "/accounts/login/?next=/accounts/profile/")

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
            'patron_title': 'TestPatron',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
        response = self.client.post(reverse('create_creator_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/")
        self.assertEqual(CreatorProfile.objects.count(), 1)
        creator = CreatorProfile.objects.get(user=self.user)
        self.assertEqual(creator.patron_title, 'TestPatron')
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Your profile data has been saved.")

    def test_create_default_tiers(self):
        """
        Test the creation of a default creator tiers.
        """
        self.client.force_login(self.user)
        data = {
            'patron_title': 'TestPatron',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
        # create a creator profile
        self.client.post(reverse('create_creator_profile'), data)
        creator = CreatorProfile.objects.get(user=self.user)
        # query the view_tiers view
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        self.assertIn({"name": "Onetime"}, tiers.values('name'))
        self.assertIn({"name": "Fan"}, tiers.values('name'))
        self.assertIn({"name": "Superfan"}, tiers.values('name'))
        self.assertEqual(tiers.count(), 3)
        self.assertEqual(tiers[0]['name'], 'Onetime')
        self.assertEqual(tiers[1]['name'], 'Fan')
        self.assertEqual(tiers[2]['name'], 'Superfan')
        self.assertEqual(tiers[0]['price'], 100)
        self.assertEqual(tiers[1]['price'], 25)
        self.assertEqual(tiers[2]['price'], 50)
        desc = {
            "one": "Make a one-time contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "You can edit your default tiers.")

        response = self.client.get(reverse('patron:tiers'))
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("You can edit your default tiers.", messages)
