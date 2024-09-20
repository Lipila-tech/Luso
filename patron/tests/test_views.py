from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import Mock, patch
import json
from django.contrib.auth import get_user_model
# Custom models
from accounts.models import CreatorProfile
from patron.models import Tier, TierSubscriptions, SubscriptionPayments, Contributions
from.factory import UserFactory, CreatorProfileFactory
from lipila.utils import get_patron_title_by_creator


class TestSubscription(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.staff_user = UserFactory(username='staffuser', email='user11@bot.test')
        cls.creator_user1 = UserFactory(username='testcreator1', email='use2r@bot.test')
        cls.creator_user2 = UserFactory(username='testcreator2', email='use3r@bot.test')
        cls.user1 = UserFactory(username='test_user', email='user5@bot.test')
        cls.creator1_obj = CreatorProfileFactory(user=cls.creator_user1, patron_title='test1')
        cls.creator2_obj = CreatorProfileFactory(user=cls.creator_user2, patron_title='test2')
        Tier().create_default_tiers(cls.creator1_obj)  # creator 1 tiers
        Tier().create_default_tiers(cls.creator2_obj)  # creator 2 tiers
        cls.tiers_1 = Tier.objects.filter(creator=cls.creator1_obj).values()
        cls.tiers_2 = Tier.objects.filter(creator=cls.creator2_obj).values()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        get_user_model().objects.all().delete()

    def test_join_view_valid(self):
        self.client.force_login(self.user1)
        url = reverse('patron:join_tier', kwargs={
                      'tier_id': self.tiers_1[0]['id']})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Welcome! You Joined my Buy me a coffee patrons.")
        self.assertEqual(TierSubscriptions.objects.count(), 1)

    def test_get_creator_patrons(self):
        self.client.force_login(self.creator_user1)
        user1 = get_user_model().objects.create(
            username='testuser1', email='user12@bot.test', password='password')
        user2 = get_user_model().objects.create(
            username='testuser_2', email='user2@bot.test', password='password')
        user3 = get_user_model().objects.create(
            username='testuser3', email='user3@bot.test', password='password')
        user4 = get_user_model().objects.create(
            username='testuser4', email='user4@bot.test', password='password')
        user5 = get_user_model().objects.create(
            username='testuser_5', email='user55@bot.test', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[2]['id'])
        tier3 = Tier.objects.get(pk=self.tiers_2[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)
        TierSubscriptions.objects.create(patron=user2, tier=tier1)
        TierSubscriptions.objects.create(patron=user3, tier=tier2)
        TierSubscriptions.objects.create(patron=user4, tier=tier3)
        TierSubscriptions.objects.create(patron=user5, tier=tier2)
        response = self.client.get(reverse('patron:patrons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('patron/admin/pages/view_patrons.html')
        self.assertEqual(TierSubscriptions.objects.count(), 5)

    def test_get_creator_home(self):
        self.client.force_login(self.user1)
        title = get_patron_title_by_creator(self.creator1_obj)
        url = reverse('creator_index', kwargs={
                      'title': title})
        user1 = get_user_model().objects.create(
            username='testuser6', email='user6@bot.test', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=self.user1, tier=tier1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('lipila.views.query_collection')
    @patch('lipila.views.get_api_user')
    def test_send_money_subscription_valid(self, api_user, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response
        api_user.return_value = self.staff_user

        user1 = get_user_model().objects.create(
            username='testuser7', email='user7@bot.test', password='password')
        self.client.force_login(user1)
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)

        url = reverse('send_money_id', kwargs={'type':'subscription', 'id':tier1.id})
        data = {'amount': '100', 'payer_account_number': '0966443322',
                'wallet_type': 'mtn', 'description': 'testdescription'}

        # data = json.dumps(data)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Payment of K100.00 successful!')
        self.assertEqual(SubscriptionPayments.objects.count(), 1)

    
        
    def test_subscription_history(self):
        user1 = get_user_model().objects.create(
            username='testuser9', email='user9@bot.test', password='password')
        self.client.force_login(user1)
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)
        url = reverse('subscriptions_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('patron/admin/pages/payments_made.html')


class TestPatronViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.client = Client()
        cls.creatoruser1 = get_user_model().objects.create(
            username='testuser_1', email='user@bot.test', password='password')
        cls.user2 = get_user_model().objects.create(
            username='testuser2', email='user1@bot.test', password='password')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        get_user_model().objects.all().delete()


    def test_redirect_unauthenticated_user(self):
        """
        Test that an unathenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('patron:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/patron/accounts/profile/")

    def test_get_profile(self):
        """
        Test that a user is redirected to choose a profile type
        view, if they don't have one.
        """
        self.client.force_login(self.creatoruser1)
        response = self.client.get(reverse('patron:profile'))
        self.assertEqual(response.status_code, 200)


    def test_create_creator_profile(self):
        """
        Test the creation of a new user.creator_profile
        """
        self.client.force_login(self.creatoruser1)
        data = {
            'patron_title': 'TestPatron',
            'location': '01',
            'creator_category': 'artist',
            'adults_group':'True',
            'country': 'zambia'
        }
        response = self.client.post(
            reverse('patron:create_creator_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/patron/my-tiers")
        self.assertEqual(CreatorProfile.objects.count(), 1)
        creator = CreatorProfile.objects.get(user=self.creatoruser1)
        self.assertEqual(creator.patron_title, 'TestPatron')
        res = self.client.get(reverse('patron:profile'))
        self.assertEqual(res.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Your profile data has been saved.")
        has_group = get_user_model().objects.get(username='testuser_1')
        self.assertTrue(has_group.has_group)


    def test_create_default_tiers(self):
        """
        Test the creation of a default creator tiers.
        """
        self.client.force_login(self.creatoruser1)
        data = {
            'patron_title': 'TestPatron23',
            'location': '01',
            'creator_category': 'artist',
            'adults_group':'True',
            'country': 'zambia'
        }
        # create a creator profile
        self.client.post(reverse('patron:create_creator_profile'), data)
        creator = CreatorProfile.objects.get(user=self.creatoruser1)
        # query the view_tiers view
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        self.assertIn({"name": "Buy me a coffee"}, tiers.values('name'))
        
        self.assertEqual(tiers.count(), 1)
        self.assertEqual(tiers[0]['name'], 'Buy me a coffee')
        self.assertEqual(tiers[0]['price'], 10)
        
        desc = {
            "one": "Make a one-time Contribution to support my work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tier created. You can update the details.")

        response = self.client.get(reverse('patron:tiers'))
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("Default tier created. You can update the details.", messages)

    def test_create_default_tiers_different_user_tier_exists(self):
        """
        Test the creation of a default creator tiers.
        """
        data = {
            'patron_title': 'TestPatron12',
            'location': '01',
            'creator_category': 'artist',
            'adults_group':'True',
            'country': 'zambia'
        }
        creator1 = CreatorProfile.objects.create(
            user=self.creatoruser1, patron_title='testpatron', about='test', creator_category='musician')
        Tier().create_default_tiers(creator1)
        # login user 2 and create tiers
        self.client.force_login(self.user2)
        self.client.post(reverse('patron:create_creator_profile'), data)
        creator2 = CreatorProfile.objects.get(user=self.user2)
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator2).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        desc = {
            "one": "Make a one-time Contribution to support my work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")
