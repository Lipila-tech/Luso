from django.test import TestCase, Client
from django.contrib.auth.models import User
from patron.models import Tier, TierSubscriptions, Payments, Contributions, WithdrawalRequest
from django.urls import reverse

# custom modules
from patron import helpers
from accounts.models import CreatorProfile
from patron.templatetags.patron_tags import is_patron_subscribed


class TestHelperFunctions(TestCase):
    def setUp(self):
        self.client = Client()
        # Create creator users, their creator profiles and thir tiers
        self.creator_user1 = User.objects.create(
            username='testcreator1', password='password')
        self.creator1_obj = CreatorProfile.objects.create(
            user=self.creator_user1, patron_title='testpatron1', about='test', creator_category='musician')
        
        self.creator_user2 = User.objects.create(
            username='testcreator2', password='password')
        self.creator2_obj = CreatorProfile.objects.create(
            user=self.creator_user2, patron_title='testpatron2', about='test', creator_category='musician')
        
        # Create the tiers and filter objects
        Tier().create_default_tiers(self.creator1_obj)  # creator 1 tiers
        Tier().create_default_tiers(self.creator2_obj)  # creator 2 tiers
        self.tiers_1 = Tier.objects.filter(creator=self.creator1_obj).values()
        self.tiers_2 = Tier.objects.filter(creator=self.creator2_obj).values()
        
        # Create patron users
        self.user1 = User.objects.create(
            username='testuser', password='password')
        self.user2 = User.objects.create(
            username='patronusertest', password='password')

    def test_get_creator_url(self):
        domain = 'localhost:8000'
        url = helpers.get_creator_url('index', self.creator1_obj.patron_title, domain=domain)
        self.assertEqual(url, f'{domain}/testpatron1')

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
        """
        Test template tag function.
        """
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
        is_patrons1 = is_patron_subscribed(user1, tier1.id)
        is_patrons2 = is_patron_subscribed(user3, tier3.id)
        self.assertEqual(is_patrons1, True)
        self.assertEqual(is_patrons2, False)

    def test_calculate_total_payments(self):
        """
        Test if the function returns the expected values.
        """
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        subscription1  = TierSubscriptions.objects.create(patron=self.user1, tier=tier1)
        subscription2  = TierSubscriptions.objects.create(patron=self.user2, tier=tier2)
        Payments.objects.create(subscription=subscription1, amount=200)
        Payments.objects.create(subscription=subscription2, amount=200)
        total_amounts1 = helpers.calculate_total_payments(self.creator1_obj)
        total_amounts2 = helpers.calculate_total_payments(self.creator2_obj)
        self.assertEqual(total_amounts1, 400)
        self.assertEqual(total_amounts2, 0)
        
    def test_calculate_total_contributions(self):
        """
        Test if the function calculates and returns the expected values.
        """
        contri1  = Contributions.objects.create(creator=self.creator_user1, patron=self.user1, amount=100)
        contri2  = Contributions.objects.create(creator=self.creator_user1, patron=self.user2, amount=100)
        contri3  = Contributions.objects.create(creator=self.creator_user2, patron=self.user1, amount=100)
        self.assertEqual(helpers.calculate_total_contributions(self.creator_user1), 200)
        self.assertEqual(helpers.calculate_total_contributions(self.creator_user2), 100)

    def test_calculate_total_withdrawals(self):
        """
        Test if the function calculates and returns the expected values.
        """
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        subscription1  = TierSubscriptions.objects.create(patron=self.user1, tier=tier1)
        subscription2  = TierSubscriptions.objects.create(patron=self.user2, tier=tier2)
        Payments.objects.create(subscription=subscription1, amount=200)
        Payments.objects.create(subscription=subscription2, amount=200)
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=100, status='success')
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=50, status='success')
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=50)
        WithdrawalRequest.objects.create(creator=self.creator2_obj, amount=100)
        self.assertEqual(helpers.calculate_total_withdrawals(self.creator1_obj), 150)
        self.assertEqual(helpers.calculate_total_withdrawals(self.creator2_obj), 0.0)


    def test_calculate_creators_balance(self):
        """
        Test if the function calculates and returns the expected values.
        """
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        subscription1  = TierSubscriptions.objects.create(patron=self.user1, tier=tier1)
        Payments.objects.create(subscription=subscription1, amount=200)
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=100, status='success')
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=100, status='success')
        Contributions.objects.create(creator=self.creator_user1, patron=self.user1, amount=100)
        self.assertEqual(helpers.calculate_creators_balance(self.creator1_obj), 100)
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=50, status='success')
        self.assertEqual(helpers.calculate_creators_balance(self.creator1_obj), 50)



