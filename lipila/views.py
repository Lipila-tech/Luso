from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
import requests
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
    SubscriptionPaymentsForm,
    PaymentForm,
)

from django.core.mail import send_mail

from .utils import query_collection, process_mtn_payment
from django.http import HttpResponseRedirect
# Custom Models
from api.utils import generate_transaction_id
from lipila.utils import (
    apology, get_lipila_contact_info,
    get_lipila_index_page_info, get_testimonials, get_lipila_about_info,
    query_disbursement, check_payment_status)
from accounts.models import CreatorProfile
from patron.models import (WithdrawalRequest, SubscriptionPayments,
                           ProcessedWithdrawals, Tier, TierSubscriptions, Transfer)
from patron.utils import calculate_creators_balance
from .utils import get_api_user, get_braintree_client_token, braintree_gateway
from .models import CustomerMessage
from .utils import (
    is_patron_title_valid, get_tier_by_patron_title, get_tier_subscription_by_id_patron)



def custom_404_view(request, exception):
    data = {'message': 'That page was not found', 'status': 404}
    return apology(request, data)


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


def about(request):
    return render(request, 'about.html')

def creator_index(request, title):
    """
    renders a creators home page.

    Args:
        request: The incoming HTTP request object.
        creator: The username of the creator the user wants to view.

    Returns:
        A rendered response with the creator details.
    """
    is_valid = is_patron_title_valid(title)

    if is_valid:
        from lipila.utils import get_creator_by_patron_title, get_patron_profile_by_patron_title
        from patron.utils import get_creator_subscribers, get_creator_url
        from file_manager.utils import get_user_files

        creator = get_creator_by_patron_title(title)
        tiers = Tier.objects.filter(creator=creator.creatorprofile).values()
        patrons = get_creator_subscribers(creator.creatorprofile)

        url = get_creator_url('index', title, domain='localhost:8000')

        files = get_user_files(creator, 'all')

        if creator.username == request.user.username:

            messages.info(request, "Viewing page as Visitor")

        context = {'creator': creator.creatorprofile,
                   'tiers': tiers,
                   'patrons': len(patrons),
                   'media': files,
                   'url': url,
                   }
        return render(request, 'patron/admin/profile/creator_home.html', context)
    data = {'message': 'Sorry! no Patron matched that name.', 'status': 404}
    return apology(request, data)


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
                reference = withdrawal_request.reason
                request_date = withdrawal_request.request_date
                transaction_id = withdrawal_request.transaction_id

                # Process withdrawal (initiate payout using lipila api)
                payload = {
                    'amount': amount,
                    'wallet_type': wallet_type,
                    'send_money_to': send_money_to,
                    'reference': reference
                }
                response = query_disbursement(
                    request.user, 'POST', transaction_id, data=payload)

                if response.status_code == 202:
                    withdrawal_request.status = 'accepted'
                    withdrawal_request.processed_date = timezone.now()
                    withdrawal_request.save()

                    # save to processed withdrawals
                    processed_withdrawals.approved_by = request.user
                    processed_withdrawals.status = 'accepted'
                    processed_withdrawals.transaction_id = transaction_id
                    processed_withdrawals.request_date = request_date
                    processed_withdrawals.save()
                    # consider making an async function
                    if check_payment_status(transaction_id, 'dis') == 'success':
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
                transaction_id = withdrawal_request.transaction_id

                withdrawal_request.status = 'rejected'
                withdrawal_request.processed_date = timezone.now()
                withdrawal_request.save()

                # Process withdraw
                processed_withdrawals.processed_date = timezone.now()
                processed_withdrawals.request_date = request_date
                processed_withdrawals.transaction_id = transaction_id
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
        transaction_id = generate_transaction_id()  # generate uniq transaction id
        withdrawal_request = form.save(commit=False)
        # Assuming user is authenticated creator
        withdrawal_request.creator = self.request.user.creatorprofile
        withdrawal_request.status = 'pending'
        withdrawal_request.transaction_id = transaction_id
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
    success_url = reverse_lazy('patron:subscriptions')

    def get_object(self, queryset=None):
        tier_id = self.kwargs.get('tier_id')
        if tier_id:
            return get_object_or_404(TierSubscriptions, tier__id=tier_id, patron=self.request.user)
        return None


class TierReadView(BSModalReadView):
    model = Tier
    template_name = 'lipila/modals/view_tier.html'


def tiers(request):
    data = {}
    if request.method == 'GET':
        tiers = Tier.objects.filter(creator=request.user.creatorprofile)
        data['table'] = render_to_string(
            'reusables/_tiers_table.html',
            {'tiers': tiers},
            request=request
        )
        return JsonResponse(data)


@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
@login_required
def transfer(request):
    transfers = Transfer.objects.filter(payer=request.user)
    return render(request, 'lipila/actions/transfer.html', {'transfers': transfers})


@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
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


@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
@login_required
def staff_users(request):
    total_users = len(get_user_model().objects.all())
    total_creators = len(CreatorProfile.objects.all())
    pending_withdrawals = len(WithdrawalRequest.objects.filter(
        Q(status='pending') | Q(status='failed')))
    messages = len(CustomerMessage.objects.filter(is_seen=False))
    context = {
        'all_users': total_users,
        'all_creators': total_creators,
        'pending_withdrawals': pending_withdrawals,
        'updated_at': timezone.now(),
        'c_messages': messages,
    }
    return render(request, 'lipila/staff/home.html', context)


@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
@login_required
def customer_messages_view(request):
    messages = CustomerMessage.objects.filter(is_seen=False).order_by(
        '-timestamp')  # Fetch all messages ordered by timestamp
    return render(request, 'lipila/staff/customer_messages.html', {'c_messages': messages})


@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
@login_required
def reply_to_message_view(request, message_id):
    message = get_object_or_404(CustomerMessage, id=message_id)

    if request.method == 'POST':
        reply_subject = f"Re: {message.subject}"
        reply_message = request.POST.get('reply_message')
        sender_email = settings.DEFAULT_FROM_EMAIL

        # Send email
        send_mail(
            reply_subject,
            reply_message,
            sender_email,
            [message.email],
            fail_silently=False,
        )
        message.is_seen = True
        message.handler = request.user
        message.save()
        messages.success(request, 'Reply sent')

        # Redirect or show a success message after replying
        return render(request, 'lipila/staff/reply_success.html', {'message': message})

    return render(request, 'lipila/staff/reply_message.html', {'message': message})


@login_required
@user_passes_test(lambda u: u.is_staff)
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
        is_verified = CreatorProfile.objects.get(user=obj.creator).is_verified
        item = {}
        item['pk'] = obj.pk
        item['is_verified'] = is_verified
        item['creator'] = obj.creator
        item['amount'] = obj.amount
        item['status'] = obj.status
        item['account_number'] = obj.account_number
        item['wallet_type'] = obj.wallet_type
        item['request_date'] = obj.request_date
        item['transaction_id'] = obj.transaction_id
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
        items['transaction_id'] = item.withdrawal_request.transaction_id
        data.append(items)
    context = {}
    context['processed_withdrawals'] = data
    return render(request, 'lipila/staff/processed_withdrawals.html', context)


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
                request, "We have received your message. We will be in touch soon.")
            return redirect('index')  # Redirect to a success page (optional)
    else:
        messages.error(
            request, "Failed to send message")
        form = ContactForm()
        context['form'] = form
    return render(request, 'index.html', context)


# @login_required
def checkout_subscription(request, id):
    url = reverse('subscriptions_history')
    patron = request.user
    tier = get_tier_subscription_by_id_patron(id, patron)

    amount = tier.tier.price
    product = tier.tier.name
    if request.method == 'POST':
        form = SubscriptionPaymentsForm(
            request.POST, amount=amount, payee=tier)

        if form.is_valid():
            # Extract data from the form
            wallet_type = form.cleaned_data['wallet_type']
            transaction_id = generate_transaction_id()
            amount = form.cleaned_data['amount']
            msisdn = form.cleaned_data['msisdn']
            reference = form.cleaned_data['reference']
            
            if wallet_type == 'mtn':
                form.instance.transaction_id = transaction_id
                form.amount = amount
                form.save()
                # process mtn payment
                payment_data = {
                    'payer': request.user,
                    'amount': amount,
                    'transaction': 'subscription',
                    'transaction_id': transaction_id,
                    'msisdn': msisdn,
                    'reference': reference
                }
                response = process_mtn_payment(**payment_data)
                if response.status_code == 200:
                    form.instance.status = 'success'
                    form.save()
                    messages.success(
                        request, f"Payment Success: Account : { form.cleaned_data['msisdn']} amount: {amount} Wallet:{wallet_type}")
                    return redirect(url)
                else:
                    form.instance.status = 'failed'
                    form.save()
                    messages.error(
                        request, "Error: Payment failed try again later!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif wallet_type == 'airtel':
                """
                This view will make a POST request to the AirtelPaymentRequestView in the 'payments' app.
                """
                # Prepare the payload for the API call
                payload = {
                    'reference': reference,
                    'msisdn': msisdn,
                    'transaction_id': transaction_id,
                    'amount': amount
                }

                # Make the request to AirtelPaymentRequestView API
                try:
                    # Assuming the AirtelPaymentRequestView URL is /api/airtel/request-payment/
                    response = requests.post('http://localhost:8000/api/airtel/request-payment/', json=payload)

                    # Handle success
                    if response.status_code == 201:
                        data = response.json()
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Payment request initiated successfully',
                            'data': data
                        }, status=201)

                    # Handle failure
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Failed to initiate payment: {response.json().get("detail", "Unknown error")}'
                    }, status=response.status_code)

                except requests.exceptions.RequestException as e:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Request failed: {str(e)}'
                    }, status=500)
            else:
                client_token = get_braintree_client_token(request.user)
                context = {'client_token': client_token,
                           'form': form, 'amount': amount}
        else:
            form = SubscriptionPaymentsForm(amount=amount, payee=tier)
            client_token = get_braintree_client_token(request.user)
            context = {'client_token': client_token,
                       'form': form, 'amount': amount}
            messages.error(request, "Field errors!")
            return render(request, 'lipila/checkout/checkout_subscription.html', context)

    form = SubscriptionPaymentsForm(amount=amount, payee=tier)
    client_token = get_braintree_client_token(request.user)
    context = {'client_token': client_token, 'form': form,
               'amount': amount, "product": product}
    return render(request, 'lipila/checkout/checkout_subscription.html', context)



def checkout_support(request, payee):
    url = ''

    if request.method == 'POST':
          
        form = PaymentForm(
                request.POST, payee=payee)
              
        if form.is_valid():            
            form.save(commit=False)
            # extract data to send to api
            wallet_type = form.cleaned_data['wallet_type']
            reference = form.cleaned_data['reference']
            amount = form.cleaned_data['amount']
            transaction_id = generate_transaction_id()
            msisdn = form.cleaned_data['msisdn']

             # Prepare the payload for the API call
            payload = {
                'amount': amount,
                'reference': reference,
                'transaction_id': transaction_id,
                'msisdn': msisdn,
                'wallet_type': wallet_type
            }
            
            if request.user.is_authenticated:
                form.instance.authenticated_payer = request.user
                url = reverse('subscriptions_history')
            else:
                url = reverse('accounts:signup')
                try:
                    payer = form.cleaned_data['payer']
                    form.instance.anonymous_payer = payer
                except KeyError:
                    form.instance.anonymous_payer = msisdn

            # Add logic for calculating total_amount if the user checked the 'I'll generously add K2.50' box
            if 'add_contribution' in request.POST and request.POST['add_contribution'] == 'on':
                form.amount = float(amount) + 2.5
            else:
                form.amount = amount
            form.instance.transaction_id = transaction_id
            form.save()  # Now save to DB

            try:
                if wallet_type == 'mtn':
                    checkout_url = settings.LIPILA_CHECKOUT_URL_MTN
                elif wallet_type == 'airtel':
                    checkout_url = settings.LIPILA_CHECKOUT_URL_MTN

                response = requests.post(checkout_url, json=payload)
                
                if response.status_code == 201:
                    form.instance.status = 'success'
                    form.save()
                    messages.success(
                        request, f"Payment Success: Account : { form.cleaned_data['msisdn']} amount: {amount} Wallet:{wallet_type}")
                    return redirect(url)
                
                response_text = response.content.decode('utf-8')
                response_json = json.loads(response_text)
                
                msg = {'message': f'Failed to initiate payment: {response_json.get("message", "Unknown error")}', 'status':response.status_code}
                return apology(request, data=msg)
            
            except requests.exceptions.RequestException as e:
                msg = {'message': f'Failed to initiate payment: {response_json.get("message", "Unknown error")}', 'status':500}
                return apology(request, data=msg)

        else:
            form = PaymentForm(payee=payee)
            # client_token = get_braintree_client_token(request.user)
            context = {'client_token': client_token,
                       'form': form}
            messages.error(request, "Field errors!")
            return render(request, 'lipila/checkout/checkout_support.html', context)
    
    form = PaymentForm(payee=payee)
            
    client_token = get_braintree_client_token(request.user)
    context = {'client_token': client_token, 'form': form, "payee": payee}
    return render(request, 'lipila/checkout/checkout_support.html', context)


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
