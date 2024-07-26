from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import json
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from lipila.forms.forms import (
    ContactForm,
    WithdrawalModelForm,
    TierModelForm,
    ContributionsForm,
    TransferForm,
    SubscriptionPaymentsForm
)

from .utils import query_collection
from django.http import HttpResponseRedirect
# Custom Models
from api.utils import generate_reference_id
from lipila.utils import (
    apology, get_lipila_contact_info,
    get_lipila_index_page_info, get_testimonials, get_lipila_about_info,
    query_disbursement, check_payment_status)
from accounts.models import CreatorProfile
from patron.models import (WithdrawalRequest, SubscriptionPayments,
                           ProcessedWithdrawals, Tier, TierSubscriptions, Transfer)
from patron.utils import calculate_creators_balance
from .utils import get_api_user, get_braintree_client_token, braintree_gateway


# Django-bootstrap Modal forms views

class ApproveWithdrawModalView(View):
    success_url = reverse_lazy('processed_withdrawals')

    def post(self, request, pk):
        withdrawal_request_id = request.POST.get('request_id')
        if withdrawal_request_id:
            try:
                withdrawal_request = WithdrawalRequest.objects.get(
                    pk=withdrawal_request_id)
                processed_withdrawals = ProcessedWithdrawals.objects.create(
                    withdrawal_request=withdrawal_request, status='pending')

                amount = withdrawal_request.amount
                wallet_type = withdrawal_request.wallet_type
                send_money_to = withdrawal_request.account_number
                description = withdrawal_request.reason
                request_date = withdrawal_request.request_date
                reference_id = withdrawal_request.reference_id

                # Process withdrawal (initiate payout using lipila api)
                payload = {
                    'amount': amount,
                    'wallet_type': wallet_type,
                    'send_money_to': send_money_to,
                    'description': description
                }
                response = query_disbursement(
                    request.user, 'POST', reference_id, data=payload)

                if response.status_code == 202:
                    withdrawal_request.status = 'accepted'
                    withdrawal_request.processed_date = timezone.now()
                    withdrawal_request.save()

                    # save to processed withdrawals
                    processed_withdrawals.approved_by = request.user
                    processed_withdrawals.status = 'accepted'
                    processed_withdrawals.reference_id = reference_id
                    processed_withdrawals.request_date = request_date
                    processed_withdrawals.save()
                    # consider making an async function
                    if check_payment_status(reference_id, 'dis') == 'success':
                        withdrawal_request.status = 'success'
                        processed_withdrawals.status = 'success'
                        withdrawal_request.save()
                        processed_withdrawals.save()
                    messages.success(
                        request, f"Withdrawal request for {withdrawal_request.creator.user.username} approved successfully.")
                    return JsonResponse({'message': 'Ok', 'redirect_url': self.success_url})
                else:
                    withdrawal_request.status = 'failed'
                    processed_withdrawals.status = 'failed'
                    withdrawal_request.save()
                    processed_withdrawals.save()
                    messages.error(
                        request, 'Payment failed. Please try again later!')
                    return JsonResponse({'message': 'Failed', 'redirect_url': self.success_url})
            except WithdrawalRequest.DoesNotExist:
                messages.error(request, "Withdrawal request not found.")
                return redirect('approve_withdrawals')


class RejectWithdrawModalView(View):
    success_url = reverse_lazy('processed_withdrawals')

    def post(self, request, pk):
        withdrawal_request_id = request.POST.get('request_id')

        if withdrawal_request_id:
            try:
                withdrawal_request = WithdrawalRequest.objects.get(
                    pk=withdrawal_request_id)
                processed_withdrawals = ProcessedWithdrawals.objects.create(
                    withdrawal_request=withdrawal_request, status='pending')

                amount = withdrawal_request.amount
                request_date = withdrawal_request.request_date
                reference_id = withdrawal_request.reference_id

                withdrawal_request.status = 'rejected'
                withdrawal_request.processed_date = timezone.now()
                withdrawal_request.save()

                # Process withdraw
                processed_withdrawals.processed_date = timezone.now()
                processed_withdrawals.request_date = request_date
                processed_withdrawals.reference_id = reference_id
                processed_withdrawals.rejected_by = request.user
                processed_withdrawals.status = 'rejected'
                processed_withdrawals.save()
                messages.success(
                    request, f"Rejected.: Withdrawal request of K{amount} by {withdrawal_request.creator.user.username}")
                return JsonResponse({'message': 'OK', 'redirect_url': self.success_url})
            except WithdrawalRequest.DoesNotExist:
                messages.error(request, "Withdrawal request not found.")
                return redirect('approve_withdrawals')


class CreateWithdrawalRequest(BSModalCreateView):
    form_class = WithdrawalModelForm
    template_name = 'lipila/modals/request_withdraw.html'
    success_message = 'Success: created.'
    success_url = reverse_lazy('patron:withdraw_request')

    def form_valid(self, form):
        reference_id = generate_reference_id()  # generate uniq transaction id
        withdrawal_request = form.save(commit=False)
        # Assuming user is authenticated creator
        withdrawal_request.creator = self.request.user.creatorprofile
        withdrawal_request.status = 'pending'
        withdrawal_request.reference_id = reference_id
        withdrawal_request.save()
        messages.success(
            self.request,
            'Withdrawal request submitted successfully. We will review your request and process it within 2 business days.')
        return super().form_valid(form)


class TierUpdateView(BSModalUpdateView):
    model = Tier
    template_name = 'lipila/modals/edit_tier.html'
    form_class = TierModelForm
    success_message = 'Success: Tier was updated.'
    success_url = reverse_lazy('patron:profile')


class TierDeleteView(BSModalDeleteView):
    model = Tier
    template_name = 'lipila/modals/delete_tier.html'
    success_message = 'Success: Tier was deleted.'
    success_url = reverse_lazy('patron:profile')


class UnsubScribeView(BSModalDeleteView):
    model = TierSubscriptions
    template_name = 'lipila/modals/unsubscribe_tier.html'
    success_message = 'Success: You have unsubscribed.'
    success_url = reverse_lazy('patron:profile')

    def get_object(self, queryset=None):
        tier_id = self.kwargs.get('tier_id')
        if tier_id:
            return get_object_or_404(TierSubscriptions, tier__id=tier_id, patron=self.request.user)
        return None


class TierReadView(BSModalReadView):
    model = Tier
    template_name = 'lipila/modals/view_tier.html'



class SendMoneyView(BSModalCreateView):
    template_name = 'lipila/modals/send_money.html'
    success_url = 'subscriptions_history'
    success_message = 'Success: Subscription paid'

    def get_form_class(self):
        transaction_type = self.kwargs.get('type')
        if transaction_type == 'contribution':
            return ContributionsForm
        elif transaction_type == 'subscription':
            return SubscriptionPaymentsForm
        elif transaction_type == 'transfer':
            return TransferForm
        return super().get_form_class()

    def form_valid(self, form):

        wallet_type = form.cleaned_data['wallet_type']

        if wallet_type != 'mtn':
            messages.error(
                self.request, 'Sorry only mtn is suported at the moment')
            # redirect user to the same page
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        # Define variables
        transaction_type = self.kwargs.get('type')
        amount = ''
        payee = ''
        payer_account_number = form.cleaned_data['payer_account_number']
        description = form.cleaned_data['description']
        payer = get_user_model().objects.get(username=self.request.user)
        reference_id = generate_reference_id()  # generate uniq transaction id

        if transaction_type == 'contribution':
            payee = get_user_model().objects.get(pk=self.kwargs.get('id'))
            amount = form.cleaned_data['amount']
            self.success_url = reverse_lazy('contributions_history')
        elif transaction_type == 'subscription':
            payee = TierSubscriptions.objects.get(
                tier=self.kwargs.get('id'), patron=payer)
            amount = TierSubscriptions.objects.get(
                tier=self.kwargs.get('id')).tier.price
            self.success_url = reverse_lazy('subscriptions_history')
        elif transaction_type == 'transfer':
            payee = form.cleaned_data['send_money_to']
            amount = form.cleaned_data['amount']
            self.success_url = reverse_lazy('transfers_history')

        # Populate fields
        form.instance.reference_id = reference_id
        form.instance.payee = payee
        form.instance.amount = amount

        if transaction_type == 'transfer' or transaction_type == 'contribution':
            form.instance.payer = payer

        # Manually save the form
        self.object = form.save()

        payload = {
            'amount': amount,
            'wallet_type': wallet_type,
            'payer_account_number': payer_account_number,
            'description': description
        }

        api_user = get_api_user()

        response = query_collection(
            api_user.username, 'POST', reference_id, data=payload)
        if response.status_code == 202:
            form.instance.status = 'accepted'
            messages.success(
                self.request, f"Payment of K{amount} successful!")
            if check_payment_status(reference_id, 'col') == 'success':
                form.instance.status = 'success'
            self.object = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            form.instance.status = 'failed'
            # Manually save the form
            self.object = form.save()
            messages.error(
                self.request, 'Payment failed. Please try again later!')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        messages.error(self.request, f"Invalid data sent")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


def tiers(request):
    data = {}
    if request.method == 'GET':
        tiers = Tier.objects.filter(creator=request.user.creatorprofile)
        data['table'] = render_to_string(
            '_tiers_table.html',
            {'tiers': tiers},
            request=request
        )
        return JsonResponse(data)


@login_required
def transfer(request):
    transfers = Transfer.objects.filter(payer=request.user)
    return render(request, 'lipila/actions/transfer.html', {'transfers': transfers})


@login_required
def transfers_history(request):
    """
    Retrieves an authenticated Users transfers payment history.
    """
    context = {}
    # Get a patron users history
    payments = Transfer.objects.filter(payer=request.user)
    context['transfers'] = payments
    return render(request, 'lipila/pages/transfers_made.html', context)


@login_required
def staff_users(request):
    total_users = len(get_user_model().objects.all())
    total_creators = len(CreatorProfile.objects.all())
    total_payments = len(SubscriptionPayments.objects.all())
    context = {
        'all_users': total_users,
        'all_creators': total_creators,
        'total_payments': total_payments,
        'updated_at': timezone.now()
    }
    return render(request, 'lipila/staff/home.html', context)


@login_required
# @user_passes_test(lambda u: u.is_staff)
def approve_withdrawals(request):
    """
    Renders a table that lists all withdraw (pending or failed) requests.

    Args:
        request: The incoming HTTP request object
    """
    pending_requests = WithdrawalRequest.objects.filter(
        Q(status='pending') | Q(status='failed'))
    data = []
    for obj in pending_requests:
        item = {}
        item['pk'] = obj.pk
        item['creator'] = obj.creator
        item['amount'] = obj.amount
        item['status'] = obj.status
        item['account_number'] = obj.account_number
        item['wallet_type'] = obj.wallet_type
        item['request_date'] = obj.request_date
        item['reference_id'] = obj.reference_id
        item['balance'] = calculate_creators_balance(obj.creator)
        data.append(item)
    context = {}
    context['pending_requests'] = data
    return render(request, 'lipila/staff/approve_withdrawals.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
def processed_withdrawals(request):
    """
    Renders a table that lists all processed withdrawal requests.

    Args:
        request: The incoming HTTP request object
    """
    processed_withdrawals = ProcessedWithdrawals.objects.filter(
        Q(approved_by=request.user) | Q(rejected_by=request.user))
    data = []
    for item in processed_withdrawals:
        items = {}
        items['creator'] = item.withdrawal_request.creator
        items['amount'] = item.withdrawal_request.amount
        items['status'] = item.status
        items['request_date'] = item.request_date
        items['processed_date'] = item.processed_date
        items['reference_id'] = item.withdrawal_request.reference_id
        data.append(items)
    context = {}
    context['processed_withdrawals'] = data
    return render(request, 'lipila/staff/processed_withdrawals.html', context)


# Lipila informational public views
def index(request):
    context = {}
    form = ContactForm()
    contact_info = get_lipila_contact_info()
    lipila_index = get_lipila_index_page_info()
    testimonial = get_testimonials()
    about = get_lipila_about_info()
    context['form'] = form
    context['contact'] = contact_info['contact']
    context['lipila'] = lipila_index['lipila']
    context['about'] = about['about']
    context['testimony'] = testimonial

    return render(request, 'index.html', context)


def service_details(request):
    return render(request, 'UI/services-details.html')


def portfolio_details(request):
    return render(request, 'UI/portfolio-details.html')


def pages_faq(request):
    return render(request, 'lipila/pages/pages_faq.html')


def pages_terms(request):
    return render(request, 'lipila/pages/pages_terms.html')


def pages_privacy(request):
    return render(request, 'lipila/pages/pages_privacy.html')


def contact(request):
    context = get_lipila_contact_info()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save contact information to the database
            messages.success(
                request, "Your message has been sent successfully")
            return redirect('index')  # Redirect to a success page (optional)
    else:
        messages.error(
            request, "Failed to send message")
        form = ContactForm()
        context['form'] = form
    return render(request, 'index.html', context)


@login_required
def kyc(request):
    return render(request, 'lipila/admin/kyc.html')


# Braintree developer api

def create_purchase(request):
    if request.method == 'POST':
        # Parse the JSON payload
        data = json.loads(request.body)

        # Extract the nonce and deviceData
        nonce_from_the_client = data.get('nonce')
        device_data = data.get('deviceData')
        
        result = braintree_gateway.transaction.sale({
            'amount': '45.00',
            'payment_method_nonce': nonce_from_the_client,
            "device_data": device_data,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            messages.success(request, "Payment completed")
            return JsonResponse({'status': 'success', 'nonce': nonce_from_the_client, 'device_data': device_data})
        else:
            messages.error(request, "Payment payment failed")
            return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

    client_token = get_braintree_client_token(request.user)
    context = {'client_token': client_token}
    return render(request, 'lipila/checkout/paypal.html', context)



def checkout(request):
    form = SubscriptionPaymentsForm()
    client_token = get_braintree_client_token(request.user)
    context = {'client_token': client_token, 'form':form, 'amount':100}
    return render(request, 'lipila/checkout/checkout.html', context)