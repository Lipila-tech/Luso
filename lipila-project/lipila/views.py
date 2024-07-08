from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework.response import Response
import json
from django.db.models import Q
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
    SendMoneyForm
)
from .utils import query_collection
from patron.models import Contributions
from django.http import HttpResponseRedirect
# Custom Models
from api.utils import generate_reference_id
from lipila.utils import (
    apology, get_lipila_contact_info,
    get_lipila_index_page_info, get_testimonials, get_lipila_about_info,
    query_disbursement, check_payment_status, save_payment)
from accounts.models import CreatorProfile
from patron.models import (WithdrawalRequest, SubscriptionPayments,
                           ProcessedWithdrawals, Tier, TierSubscriptions, Transfer)
from patron.utils import calculate_creators_balance


# Django-bootstrap Modal forms views
class CreateWithdrawalRequest(BSModalCreateView):
    template_name = 'lipila/modals/request_withdraw.html'
    form_class = WithdrawalModelForm
    success_message = 'Success: created.'
    success_url = reverse_lazy('index')


class TierUpdateView(BSModalUpdateView):
    model = Tier
    template_name = 'lipila/modals/edit_tier.html'
    form_class = TierModelForm
    success_message = 'Success: Tier was updated.'
    success_url = reverse_lazy('index')


class TierDeleteView(BSModalDeleteView):
    model = Tier
    template_name = 'lipila/modals/delete_tier.html'
    success_message = 'Success: Tier was deleted.'
    success_url = reverse_lazy('index')


class UnsubScribeView(BSModalDeleteView):
    model = TierSubscriptions
    template_name = 'lipila/modals/unsubscribe_tier.html'
    success_message = 'Success: You have unsubscribed.'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        tier_id = self.kwargs.get('tier_id')
        if tier_id:
            return get_object_or_404(TierSubscriptions, tier__id=tier_id, patron=self.request.user)
        return None


class TierReadView(BSModalReadView):
    model = Tier
    template_name = 'lipila/modals/view_tier.html'


class SendMoneyView(BSModalFormView):
    template_name = 'lipila/modals/send_money.html'
    form_class = SendMoneyForm
    success_url = 'patron:contributions_history'

   
    def form_valid(self, form):
        transaction_type = self.kwargs.get('type')
        amount = form.cleaned_data['amount']
        network_operator = form.cleaned_data['network_operator']
        payer_account_number = form.cleaned_data['payer_account_number']
        description = form.cleaned_data['description']

        reference_id = generate_reference_id()
        payer = User.objects.get(username=self.request.user)
        payee = ''
        payee_account_number = ''
        model_class = ''
        
        if transaction_type == 'contribution':
            model_class = Contributions
            payee = User.objects.get(pk=self.kwargs.get('id'))
        elif transaction_type == 'payment':
            model_class = SubscriptionPayments
            payee = TierSubscriptions.objects.get(tier=self.kwargs.get('id'), patron=self.request.user)
        else:
            payee_account_number = form.cleaned_data['payee_account_number']
            model_class = Transfer

        if network_operator != 'mtn':
            messages.error(
                self.request, 'Sorry only mtn is suported at the moment')
            # redirect user to the same page
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        # Save the payment using the utility function
        payment = save_payment(
            model_class,
            reference_id=reference_id,
            amount=amount,
            payer_account_number=payer_account_number,
            payee_account_number=payee_account_number,
            network_operator=network_operator,
            description=description,
            payer=payer,
            payee=payee
        )

        payload = {
            'amount': amount,
            'network_operator': network_operator,
            'payer_account_number': payer_account_number,
            'description': description
        }

        api_user = User.objects.get(pk=1)

        
        response = query_collection(
            api_user.username, 'POST', reference_id, data=payload)
        if response.status_code == 202:
            payment.status = 'accepted'
            payment.save()
            if check_payment_status(reference_id, 'col') == 'success':
                payment.status = 'success'
                payment.save()
            messages.success(
                self.request, f"Payment of K{payment.amount} successful!")
            return redirect(reverse_lazy(self.success_url))
        else:
            payment.status = 'failed'
            payment.save()
            messages.error(
                self.request, 'Payment failed. Please try again later!')
            return redirect(reverse_lazy(self.success_url))

    def form_invalid(self, form):
        messages.error(self.request, f"Invalid data sent")
        return super().form_valid(form)


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

# Lipila staff users views


@login_required
def staff_users(request, user):
    total_users = len(User.objects.all().order_by('date_joined'))
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
@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
def approve_withdrawals(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')  # Decode bytes to string
        data = json.loads(raw_data)  # Parse JSON data
        withdrawal_request_id = data['request_id']
        action = data['action']
        amount = data['amount']
        payee_account_number = data['payee_account_number']
        description = data['description']
        network_operator = data['network_operator']

        if withdrawal_request_id and action:
            try:
                withdrawal_request = WithdrawalRequest.objects.get(
                    pk=withdrawal_request_id)
                processed_withdrawals = ProcessedWithdrawals.objects.create(
                    withdrawal_request=withdrawal_request, status='pending')
                reference_id = generate_reference_id()

                if action == 'approve':
                    # Process withdrawal (initiate payout using lipila api)
                    payload = {
                        'amount': amount,
                        'network_operator': network_operator,
                        'payee_account_number': payee_account_number,
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
                        processed_withdrawals.save()
                        # consider making an async function
                        if check_payment_status(reference_id, 'dis') == 'success':
                            withdrawal_request.status = 'success'
                            processed_withdrawals.status = 'success'
                            withdrawal_request.save()
                            processed_withdrawals.save()
                        messages.success(
                            request, f"Withdrawal request for {withdrawal_request.creator.user.username} approved successfully.")
                        return JsonResponse({'message': 'Payment initiated successfully'})
                    else:
                        withdrawal_request.status = 'failed'
                        processed_withdrawals.status = 'failed'
                        withdrawal_request.save()
                        processed_withdrawals.save()
                        messages.error(
                            request, 'Payment failed. Please try again later!')
                        return JsonResponse({'message': 'Payment failed', 'reference_id': reference_id})
                elif action == 'reject':
                    rejected_reason = description
                    withdrawal_request.status = 'rejected'
                    withdrawal_request.reason = rejected_reason
                    withdrawal_request.processed_date = timezone.now()
                    withdrawal_request.save()

                    # save to processed withdrawals
                    processed_withdrawals.rejected_by = request.user
                    processed_withdrawals.status = 'rejected'
                    processed_withdrawals.reason = rejected_reason
                    processed_withdrawals.save()
                    messages.success(
                        request, f"Withdrawal request for {withdrawal_request.creator.user.username} has been rejected.")
                    return JsonResponse({'message': 'Payment has been rejected successfully'})
                else:
                    messages.error(request, "Invalid action specified.")
                return redirect('approve_withdrawals')
            except WithdrawalRequest.DoesNotExist:
                messages.error(request, "Withdrawal request not found.")
                return redirect('approve_withdrawals')
        messages.error(request, "Withdrawal id or amount missing")
        return redirect('approve_withdrawals')
    pending_requests = WithdrawalRequest.objects.filter(
        Q(status='pending') | Q(status='failed') | Q(status='rejected'))
    data = []
    for obj in pending_requests:
        item = {}
        item['pk'] = obj.pk
        item['creator'] = obj.creator
        item['amount'] = obj.amount
        item['status'] = obj.status
        item['account_number'] = obj.account_number
        item['network_operator'] = obj.network_operator
        item['request_date'] = obj.request_date
        item['balance'] = calculate_creators_balance(obj.creator)
        data.append(item)
    context = {}
    context['pending_requests'] = data
    return render(request, 'lipila/staff/approve_withdrawals.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)  # Only allow staff users
def processed_withdrawals(request):
    processed_withdrawals = ProcessedWithdrawals.objects.filter(
        Q(approved_by=request.user) | Q(rejected_by=request.user))
    data = []
    for item in processed_withdrawals:
        items = {}
        items['creator'] = item.withdrawal_request.creator
        items['amount'] = item.withdrawal_request.amount
        items['status'] = item.status
        items['approved'] = item.approved_date
        items['rejected'] = item.rejected_date
        items['reason'] = item.withdrawal_request.reason
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
