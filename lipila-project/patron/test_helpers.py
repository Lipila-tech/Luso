from django.test import TestCase, Client
from django.contrib.auth.models import User
from patron.models import Tier, TierSubscriptions
from django.urls import reverse

# custom modules
from patron import helpers
from accounts.models import CreatorProfile, PatronProfile


class TestHelperFunctions(TestCase):
    def setUp(self):
        self.client = Client()
        self.creator_user1 = User.objects.create(
            username='testcreator1', password='password')
        self.creator_user2 = User.objects.create(
            username='testcreator2', password='password')
        self.user1 = User.objects.create(
            username='testuser', password='password')
        self.creator1_obj = CreatorProfile.objects.create(
            user=self.creator_user1, patron_title='testpatron1', bio='test', creator_category='musician')
        self.creator2_obj = CreatorProfile.objects.create(
            user=self.creator_user2, patron_title='testpatron2', bio='test', creator_category='musician')
        Tier().create_default_tiers(self.creator1_obj)  # creator 1 tiers
        Tier().create_default_tiers(self.creator2_obj)  # creator 2 tiers
        self.tiers_1 = Tier.objects.filter(creator=self.creator1_obj).values()
        self.tiers_2 = Tier.objects.filter(creator=self.creator2_obj).values()

    def test_get_creator_subscribers(self):
        self.client.force_login(self.creator_user1)
        user1 = User.objects.create(
            username='testuser1', password='password')
        user2 = User.objects.create(
            username='testuser2', password='password')
        user3 = User.objects.create(
            username='testuser3', password='password')
        user4 = User.objects.create(
            username='testuser4', password='password')
        user5 = User.objects.create(
            username='testuser5', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[2]['id'])
        tier3 = Tier.objects.get(pk=self.tiers_2[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)  # 1
        TierSubscriptions.objects.create(patron=user2, tier=tier1)  # 1
        TierSubscriptions.objects.create(patron=user3, tier=tier2)  # 1
        TierSubscriptions.objects.create(patron=user4, tier=tier3)  # 2
        TierSubscriptions.objects.create(patron=user5, tier=tier2)  # 1
        patrons1 = helpers.get_creator_subscribers(self.creator1_obj)
        patrons2 = helpers.get_creator_subscribers(self.creator2_obj)
        self.assertEqual(len(patrons1), 4)
        self.assertEqual(len(patrons2), 1)
        self.assertTrue(type(patrons1), list)
        self.assertTrue(type(patrons1[0]), str)
        

    def test_check_if_patron_is_subscribed(self):
        self.client.force_login(self.creator_user1)
        user1 = User.objects.create(
            username='testuser1', password='password')
        user2 = User.objects.create(
            username='testuser2', password='password')
        user3 = User.objects.create(
            username='testuser3', password='password')
        user4 = User.objects.create(
            username='testuser4', password='password')
        user5 = User.objects.create(
            username='testuser5', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[2]['id'])
        tier3 = Tier.objects.get(pk=self.tiers_2[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)  # 1
        TierSubscriptions.objects.create(patron=user2, tier=tier1)  # 1
        TierSubscriptions.objects.create(patron=user3, tier=tier2)  # 1
        TierSubscriptions.objects.create(patron=user4, tier=tier3)  # 2
        TierSubscriptions.objects.create(patron=user5, tier=tier2)  # 1
        is_patrons1 = helpers.is_patron_subscribed(user1, tier1.id)
        is_patrons2 = helpers.is_patron_subscribed(user3, tier3.id)
        self.assertEqual(is_patrons1, True)
        self.assertEqual(is_patrons2, False)
