from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.messages import get_messages
from accounts.models import CreatorProfile
from patron.models import Contributions, SubscriptionPayments, TierSubscriptions, Transfer, Tier
from lipila.forms.forms import SendMoneyForm
from lipila.views import SendMoneyView
from unittest.mock import patch
from django.contrib.auth import get_user_model


class SendMoneyViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        get_user_model().objects.create(
            username='testuser', password='password')
        self.creator = get_user_model().objects.create_user(
            username='creatoruser', password='password')
        self.creator_user = CreatorProfile.objects.create(
            user=self.creator, patron_title='testpatron', about='test', creator_category='musician')
        self.contribution_user = get_user_model().objects.create_user(
            username='contribuser', password='password')
        self.client.login(username='contribuser', password='password')
        Tier().create_default_tiers(self.creator_user)
        self.tiers = Tier.objects.filter(creator=self.creator_user).values()
        tier1 = Tier.objects.get(pk=self.tiers[1]['id'])
        self.tier_subscription = TierSubscriptions.objects.create(
            tier=tier1, patron=self.contribution_user)

    @patch('lipila.views.generate_reference_id')
    @patch('lipila.views.query_collection')
    @patch('lipila.views.check_payment_status')
    @patch('lipila.views.save_payment')
    def test_send_money_contribution_success(self, mock_save_payment, mock_check_payment_status, mock_query_collection, mock_generate_reference_id):
        mock_generate_reference_id.return_value = 'ref123'
        mock_query_collection.return_value.status_code = 202
        mock_check_payment_status.return_value = 'success'
        mock_save_payment.return_value = Contributions(reference_id='ref123', amount=1000, payer_account_number='12345',
                                                       wallet_type='mtn', description='Test',
                                                       payer=self.contribution_user, payee=self.creator)

        url = reverse('send_money_id', kwargs={
                      'type': 'contribution', 'id': self.creator.pk})
        data = {
            'amount': 1000,
            'wallet_type': 'mtn',
            'payer_account_number': '1234556719',
            'description': 'Test'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contributions_history'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Payment of K1000 successful!')
        self.assertEqual(Contributions.objects.count(), 1)

    @patch('lipila.views.generate_reference_id')
    @patch('lipila.views.query_collection')
    @patch('lipila.views.check_payment_status')
    @patch('lipila.views.save_payment')
    def test_send_money_payment_success(self, mock_save_payment, mock_check_payment_status, mock_query_collection, mock_generate_reference_id):
        mock_generate_reference_id.return_value = 'ref123'
        mock_query_collection.return_value.status_code = 202
        mock_check_payment_status.return_value = 'success'
        mock_save_payment.return_value = SubscriptionPayments(reference_id='ref123', amount=1000, payer_account_number='12345',
                                                              description='Test', wallet_type='mtn',
                                                              payee=self.tier_subscription)

        url = reverse('send_money_id', kwargs={
                      'type': 'payment', 'id': self.tier_subscription.tier.pk})

        data = {
            'amount': 1000,
            'wallet_type': 'mtn',
            'payer_account_number': '12345',
            'description': 'Test'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patron:subscriptions_history'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Payment of K1000 successful!')

    @patch('lipila.views.generate_reference_id')
    @patch('lipila.views.query_collection')
    @patch('lipila.views.check_payment_status')
    @patch('lipila.views.save_payment')
    def test_send_money_transfer_success(self, mock_save_payment, mock_check_payment_status, mock_query_collection, mock_generate_reference_id):
        mock_generate_reference_id.return_value = 'ref123'
        mock_query_collection.return_value.status_code = 202
        mock_check_payment_status.return_value = 'success'
        mock_save_payment.return_value = Transfer(reference_id='ref123', amount=1000, payer_account_number='12345',
                                                  wallet_type='mtn', description='Test',
                                                  payer=self.contribution_user, send_money_to='98765')

        url = reverse('send_money_transfer', kwargs={'type': 'transfer'})
        data = {
            'amount': 1000,
            'wallet_type': 'mtn',
            'payer_account_number': '12345',
            'send_money_to': '98765',
            'description': 'Test'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('transfers_history'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Payment of K1000 successful!')
        self.assertEqual(Transfer.objects.count(), 1)

    def test_send_money_invalid_wallet_type(self):
        url = reverse('send_money_id', kwargs={
                      'type': 'payment', 'id': 1})
        data = {
            'amount': 1000,
            'wallet_type': 'airtel',
            'payer_account_number': '12345',
            'description': 'Test'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry only mtn is suported at the moment')

    def test_send_money_invalid_form(self):

        url = reverse('send_money_id', kwargs={
                      'type': 'contribution', 'id': self.contribution_user.id})
        data = {
            'amount': '',
            'wallet_type': 'mtn',
            'payer_account_number': '12345',
            'description': 'Test'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid data sent')

    def tearDown(self):
        get_user_model().objects.all().delete()
        Contributions.objects.all().delete()
        SubscriptionPayments.objects.all().delete()
        TierSubscriptions.objects.all().delete()
        Transfer.objects.all().delete()
