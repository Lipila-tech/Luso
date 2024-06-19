from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
# Custom Models
from lipila.helpers import (
    apology, get_lipila_contact_info, get_user_object,
    get_lipila_index_page_info, get_testimonials, get_lipila_about_info)
from lipila.forms.forms import ContactForm
from accounts.models import CreatorProfile
from patron.models import WithdrawalRequest, Payments, ProcessedWithdrawals
from patron.helpers import calculate_creators_balance


# Public Views
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


def send_money(request):
    context = {}
    form = request.GET
    if form:
        payee_id = form['payee_id']
        try:
            data = User.objects.get(username=payee_id)
            context['payee'] = payee_id
            context['location'] = data.city
        except User.DoesNotExist:
            context = {'message': "User id not found", }
            return render(request, '404.html', context)

    return render(request, 'UI/send_money.html', context)


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
def staff_users(request, user):
    total_users = len(User.objects.all().order_by('date_joined'))
    total_creators = len(CreatorProfile.objects.all())
    total_payments = len(Payments.objects.all())
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
        withdrawal_request_id = request.POST.get('withdrawal_request_id')
        action = request.POST.get('action')
        if withdrawal_request_id and action:
            try:
                withdrawal_request = WithdrawalRequest.objects.get(
                    pk=withdrawal_request_id)
                processed_withdrawals =  ProcessedWithdrawals.objects.create(
                    withdrawal_request=withdrawal_request)
                if action == 'approve':
                    # Process withdrawal (initiate payout using a payment processor)
                    # ...
                    withdrawal_request.status = 'success'
                    withdrawal_request.processed_date = timezone.now()
                    withdrawal_request.save()

                    # save to processed withdrawals
                    processed_withdrawals.approved_by = request.user
                    processed_withdrawals.status = 'success'
                    processed_withdrawals.save()
                    messages.success(
                        request, f"Withdrawal request for {withdrawal_request.creator.user.username} approved successfully.")
                elif action == 'reject':
                    withdrawal_request.status = 'rejected'
                    withdrawal_request.reason = 'Insufficient funds'
                    withdrawal_request.processed_date = timezone.now()
                    withdrawal_request.save()

                    # save to processed withdrawals
                    processed_withdrawals.rejected_by = request.user
                    processed_withdrawals.status = 'rejected'
                    processed_withdrawals.save()
                    messages.success(
                        request, f"Withdrawal request for {withdrawal_request.creator.user.username} rejected.")
                else:
                    messages.error(request, "Invalid action specified.")
                return redirect('approve_withdrawals')
            except WithdrawalRequest.DoesNotExist:
                messages.error(request, "Withdrawal request not found.")
                return redirect('approve_withdrawals')
    pending_requests = WithdrawalRequest.objects.filter(status='pending')
    data = []
    for obj in pending_requests:
        item = {}
        item['pk'] = obj.pk
        item['creator'] = obj.creator
        item['amount'] = obj.amount
        item['request_date'] = obj.request_date
        item['balance'] = calculate_creators_balance(obj.creator)
        data.append(item)
    context = {}
    context['pending_requests'] = data
    return render(request, 'lipila/staff/approve_withdrawals.html', context)
