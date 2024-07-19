from django.test import TestCase, Client
from django.conf import settings
from patron.models import Tier, TierSubscriptions, SubscriptionPayments, Contributions, WithdrawalRequest
from django.contrib.auth import get_user_model

# custom modules
from patron import utils
from accounts.models import CreatorProfile
from patron.templatetags.patron_tags import is_patron_subscribed
from api.utils import generate_reference_id


class TestUtilFunctions(TestCase):
    def setUp(self):
        self.client = Client()
        # Create creator users, their creator profiles and thir tiers
        self.creator_user1 = get_user_model().objects.create(
            username='testcreator1', password='password')
        self.creator1_obj = CreatorProfile.objects.create(
            user=self.creator_user1, patron_title='testpatron1', about='test', creator_category='musician')

        self.creator_user2 = get_user_model().objects.create(
            username='testcreator2', password='password')
        self.creator2_obj = CreatorProfile.objects.create(
            user=self.creator_user2, patron_title='testpatron2', about='test', creator_category='musician')

        # Create the tiers and filter objects
        Tier().create_default_tiers(self.creator1_obj)  # creator 1 tiers
        Tier().create_default_tiers(self.creator2_obj)  # creator 2 tiers
        self.tiers_1 = Tier.objects.filter(creator=self.creator1_obj).values()
        self.tiers_2 = Tier.objects.filter(creator=self.creator2_obj).values()

        # Create patron users
        self.user1 = get_user_model().objects.create(
            username='testuser', password='password')
        self.user2 = get_user_model().objects.create(
            username='patronusertest', password='password')

    def test_get_creator_url(self):
        domain = 'localhost:8000'
        url = utils.get_creator_url(
            'index', self.creator1_obj.patron_title, domain=domain)
        self.assertEqual(url, f'{domain}/testpatron1')

    def test_get_creator_subscribers(self):
        self.client.force_login(self.creator_user1)
        user1 = get_user_model().objects.create(
            username='testuser1', password='password')
        user2 = get_user_model().objects.create(
            username='testuser2', password='password')
        user3 = get_user_model().objects.create(
            username='testuser3', password='password')
        user4 = get_user_model().objects.create(
            username='testuser4', password='password')
        user5 = get_user_model().objects.create(
            username='testuser5', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[2]['id'])
        tier3 = Tier.objects.get(pk=self.tiers_2[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)  # 1
        TierSubscriptions.objects.create(patron=user2, tier=tier1)  # 1
        TierSubscriptions.objects.create(patron=user3, tier=tier2)  # 1
        TierSubscriptions.objects.create(patron=user4, tier=tier3)  # 2
        TierSubscriptions.objects.create(patron=user5, tier=tier2)  # 1
        patrons1 = utils.get_creator_subscribers(self.creator1_obj)
        patrons2 = utils.get_creator_subscribers(self.creator2_obj)
        self.assertEqual(len(patrons1), 4)
        self.assertEqual(len(patrons2), 1)
        self.assertTrue(type(patrons1), list)
        self.assertTrue(type(patrons1[0]), str)

    def test_check_if_patron_is_subscribed(self):
        """
        Test template tag function.
        """
        self.client.force_login(self.creator_user1)
        user1 = get_user_model().objects.create(
            username='testuser1', password='password')
        user2 = get_user_model().objects.create(
            username='testuser2', password='password')
        user3 = get_user_model().objects.create(
            username='testuser3', password='password')
        user4 = get_user_model().objects.create(
            username='testuser4', password='password')
        user5 = get_user_model().objects.create(
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
        subscription1 = TierSubscriptions.objects.create(
            patron=self.user1, tier=tier1)
        subscription2 = TierSubscriptions.objects.create(
            patron=self.user2, tier=tier2)
        SubscriptionPayments.objects.create(payee=subscription1, amount=200,
                                reference_id=generate_reference_id(), status='success')
        SubscriptionPayments.objects.create(payee=subscription2, amount=200,
                                reference_id=generate_reference_id(), status='success')
        total_amounts1 = utils.calculate_total_payments(self.creator1_obj)
        total_amounts2 = utils.calculate_total_payments(self.creator2_obj)
        self.assertEqual(total_amounts1, 400)
        self.assertEqual(total_amounts2, 0)

    def test_calculate_total_contributions(self):
        """
        Test if the function calculates and returns the expected values.
        """
        contri1 = Contributions.objects.create(
            payee=self.creator_user1, payer=self.user1, amount=100, reference_id=generate_reference_id(), status='pending')
        contri2 = Contributions.objects.create(
            payee=self.creator_user1, payer=self.user2, amount=100, reference_id=generate_reference_id(), status='success')
        contri3 = Contributions.objects.create(
            payee=self.creator_user2, payer=self.user1, amount=100, reference_id=generate_reference_id(), status='success')
        self.assertEqual(utils.calculate_total_contributions(
            self.creator_user1), 100)
        self.assertEqual(utils.calculate_total_contributions(
            self.creator_user2), 100)

    def test_calculate_total_withdrawals(self):
        """
        Test if the function calculates and returns the expected values.
        """
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        subscription1 = TierSubscriptions.objects.create(
            patron=self.user1, tier=tier1)
        subscription2 = TierSubscriptions.objects.create(
            patron=self.user2, tier=tier2)
        SubscriptionPayments.objects.create(
            payee=subscription1, amount=200, reference_id=generate_reference_id())
        SubscriptionPayments.objects.create(
            payee=subscription2, amount=200, reference_id=generate_reference_id())
        WithdrawalRequest.objects.create(
            creator=self.creator1_obj, amount=100, status='success')
        WithdrawalRequest.objects.create(
            creator=self.creator1_obj, amount=50, status='success')
        WithdrawalRequest.objects.create(creator=self.creator1_obj, amount=50)
        WithdrawalRequest.objects.create(creator=self.creator2_obj, amount=100)
        self.assertEqual(utils.calculate_total_withdrawals(
            self.creator1_obj), 150)
        self.assertEqual(utils.calculate_total_withdrawals(
            self.creator2_obj), 0.0)

    def test_calculate_creators_balance(self):
        """
        Test if the function calculates and returns the expected values.
        """
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        subscription1 = TierSubscriptions.objects.create(
            patron=self.user1, tier=tier1)
        SubscriptionPayments.objects.create(payee=subscription1, amount=200,
                                status='success', reference_id=generate_reference_id())
        WithdrawalRequest.objects.create(
            creator=self.creator1_obj, amount=100, status='success')
        WithdrawalRequest.objects.create(
            creator=self.creator1_obj, amount=100, status='success')
        Contributions.objects.create(
            payee=self.creator_user1, payer=self.user1, amount=100, status='success')
        self.assertEqual(utils.calculate_creators_balance(
            self.creator1_obj), 100)
        WithdrawalRequest.objects.create(
            creator=self.creator1_obj, amount=50, status='success')
        self.assertEqual(
            utils.calculate_creators_balance(self.creator1_obj), 50)
