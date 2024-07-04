from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
# custom modules
from api.utils import generate_reference_id
from accounts.models import CreatorProfile, PatronProfile
from business.models import Product
from lipila.utils import get_user_object, apology, query_collection, check_payment_status
from patron.forms.forms import (
    CreatePatronProfileForm, CreateCreatorProfileForm, EditTiersForm, WithdrawalRequestForm)
from patron.forms.forms import DefaultUserChangeForm, EditCreatorProfileForm
from lipila.forms.forms import DepositForm, ContributeForm
from patron.models import Tier, TierSubscriptions, Payments, Contributions, WithdrawalRequest
from patron.utils import (get_creator_subscribers,
                          get_creator_url, get_tier, calculate_total_payments,
                          calculate_total_contributions, calculate_total_withdrawals,
                          calculate_creators_balance)


def index(request):
    """
    Renders the Lipila Patron home page.
    """
    return render(request, 'patron/index.html')


@login_required
def profile(request):
    if request.user.is_staff:
        return redirect(reverse('staff_dashboard', kwargs={'user': request.user}))
    context = {}

    if not request.user.last_login or request.user.last_login.date() != timezone.now().date():
        messages.info(
            request, 'Please Choose your profile type.')
        return redirect('patron:choose_profile_type')
    else:
        try:
            creator = request.user.creatorprofile
            context['user'] = get_user_object(creator)
            return render(request, 'patron/admin/profile/creator-profile.html', context)
        except CreatorProfile.DoesNotExist:
            # Access creator profile using OneToOne relation
            context['user'] = get_user_object(request.user)
            return render(request, 'patron/admin/profile/patron-profile.html', context)


@login_required
def create_creator_profile(request):
    creator = request.user
    if request.method == 'POST':
        form = CreateCreatorProfileForm(
            request.POST)
        if form.is_valid():
            creator_profile = form.save(commit=False)  # Don't save yet
            creator_profile.user = creator  # Set the user based on the logged-in user
            creator_profile.save()
            messages.success(
                request, "Your profile data has been saved.")
            return redirect(reverse('patron:profile'))
        else:
            messages.error(
                request, "Failed to save profile. data")
            return render(request,
                          'patron/admin/profile/create_creator_profile.html',
                          {'form': form, 'creator': creator})
    form = CreateCreatorProfileForm()
    return render(request,
                  'patron/admin/profile/create_creator_profile.html',
                  {'form': form, 'creator': creator})


@login_required
def create_patron_profile(request):
    patron = request.user
    if request.method == 'POST':
        form = CreatePatronProfileForm(
            request.POST)
        if form.is_valid():
            patron_profile = form.save(commit=False)  # Don't save yet
            patron_profile.user = patron  # Set the user based on the logged-in user
            patron_profile.save()
            messages.success(
                request, "Your profile data has been saved.")
            return redirect(reverse('patron:profile'))
        else:
            messages.error(
                request, "Failed to save profile. data")
            return render(request,
                          'patron/admin/profile/create_creator_profile.html',
                          {'form': form, 'patron': patron})
    form = CreatePatronProfileForm()
    return render(request,
                  'patron/admin/profile/create_patron_profile.html',
                  {'form': form, 'patron': patron})


@login_required
def choose_profile_type(request):
    if request.method == 'POST':
        profile_type = request.POST.get('profile_type')
        if profile_type == 'creator':
            return redirect('patron:create_creator_profile')
        elif profile_type == 'patron':
            return redirect('patron:create_patron_profile')
        else:
            messages.error(request, 'Invalid profile type selected.')
    return render(request, 'patron/admin/profile/choose_profile_type.html')


class EditPatronProfile(LoginRequiredMixin, View):
    def get(self, request, user, *args, **kwargs):
        creator = request.user.creatorprofile
        form = EditCreatorProfileForm(instance=creator)
        return render(request,
                      'patron/admin/profile/edit_patron_info.html',
                      {'form': form, 'user': request.user})

    def post(self, request, user, *args, **kwargs):
        creator = request.user.creatorprofile
        form = EditCreatorProfileForm(
            request.POST, request.FILES, instance=creator)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated.")
            return redirect(reverse('patron:profile'))
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('patron:profile'))


class EditPersonalInfo(LoginRequiredMixin, View):
    def get(self, request, user, *args, **kwargs):
        form = DefaultUserChangeForm(instance=request.user)
        return render(request,
                      'patron/admin/profile/edit_personal_info.html',
                      {'form': form, 'user': request.user})

    def post(self, request, user, *args, **kwargs):
        form = DefaultUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated.")
            return redirect(reverse('patron:profile'))
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('patron:profile'))


@login_required
def dashboard(request, user):
    """
    Renders the appropriate dashboard based on user type (patron or creator).
    Redirects staff users to a dedicated staff dashboard.

    Args:
        request: The incoming HTTP request object.
        user: The username of the logged-in user (unused).

    Returns:
        A rendered response with the dashboard template and context.
    """
    if request.user.is_staff:
        return redirect(reverse('staff_dashboard', kwargs={'user': request.user}))
    context = {}
    now = timezone.now()
    request.session['last_login_time'] = now.strftime("%H:%M:%S")
    last_login_time = request.session.get('last_login_time')
    if last_login_time:
        context['last_login'] = last_login_time
    user_object = get_user_object(user)
    try:
        # patron summary
        subscriptions = TierSubscriptions.objects.filter(patron=user_object)
        context['summary'] = {
            'subscriptions': len(subscriptions),
            'updated_at': timezone.now
        }
        patron = request.user.patronprofile
        context['user'] = get_user_object(patron)
        return render(request, 'patron/admin/index_patron.html', context)
    except PatronProfile.DoesNotExist:
        pass
    try:
        # Creator summary
        creator = CreatorProfile.objects.get(user=request.user)
        tiers = Tier.objects.filter(creator=creator)
        patrons = get_creator_subscribers(creator)
        total_payments = calculate_total_payments(creator)
        total_contributions = calculate_total_contributions(
            User.objects.get(username=creator))
        withdrawals = calculate_total_withdrawals(creator)
        balance = calculate_creators_balance(creator)
        context['summary'] = {
            'balance': balance,
            'total_payments': total_payments + total_contributions,
            'withdrawals': withdrawals,
            'patrons': len(get_creator_subscribers(creator)),
            'tiers': len(Tier.objects.filter(creator=creator)),
            'updated_at': timezone.now,
            'last_login_time': last_login_time
        }
        creator = request.user.creatorprofile
        url = get_creator_url('index', creator, domain='localhost:8000')
        context['user'] = get_user_object(creator)
        context['url'] = url
        return render(request, 'patron/admin/index_creator.html', context)
    except CreatorProfile.DoesNotExist:
        messages.info(
            request, 'Please Choose your profile type.')
        return redirect('patron:choose_profile_type')


@login_required
def patron(request):
    """
    Retrives a users patrons.
    """
    context = {}
    creator = get_object_or_404(CreatorProfile, user=request.user)
    patrons = get_creator_subscribers(creator)
    context['patrons'] = patrons
    return render(request, 'patron/admin/pages/view_patrons.html', context)


@login_required
def view_tiers(request):
    """
    Retrives a an authenticated Creator User's tiers.
    """
    creator = CreatorProfile.objects.get(user=request.user)
    tiers = Tier.objects.filter(creator=creator).values()

    # Ensure defaults exist
    if not tiers.exists():
        Tier().create_default_tiers(creator)
        messages.info(request, "Default tiers created. Please edit them.")
    return render(request,
                  'patron/admin/pages/view_tiers.html',
                  {'user': request.user, 'tiers': tiers})


@login_required
def edit_tiers(request, tier_id):
    """
    renders a form to edit a crators tiers.

    Args:
        request: THe incoming HTTP request object.
        tiers: The tier the creator user wants to edit.
    """
    tier = get_object_or_404(Tier, pk=tier_id)
    if request.method == 'POST':
        form = EditTiersForm(request.POST, instance=tier)
        if form.is_valid():
            form.save()
            messages.success(request, "Tier Edited Successfully.")
            return redirect(reverse('patron:tiers'))
        else:
            messages.error(request, "Invalid form. Please check your data.")
        return render(request,
                      'patron/admin/actions/edit_tiers.html',
                      {'user': request.user, 'tier': tier_id, 'form': form})

    form = EditTiersForm(instance=tier)
    return render(request,
                  'patron/admin/actions/edit_tiers.html',
                  {'user': request.user, 'tier_id': tier_id, 'form': form})


def creator_home(request, creator):
    """
    renders a creator home page.

    Args:
        request: The incoming HTTP request object.
        creator: The username of the creator the user wants to view.

    Returns:
        A rendered response with the creator details.
    """
    if request.user.is_authenticated:
        patron_user = User.objects.get(username=request.user)
        creator_user = User.objects.get(username=creator)
        creator_obj = CreatorProfile.objects.get(user=creator_user.id)
        tiers = Tier.objects.filter(creator=creator_obj).values()
        patrons = get_creator_subscribers(creator_obj)
        return render(request,
                      'patron/admin/profile/creator_home_auth.html',
                      {'creator': creator_obj,
                       'tiers': tiers,
                       'patrons': len(patrons),
                       })
    else:
        creator_user = User.objects.get(username=creator)
        creator_obj = CreatorProfile.objects.get(user=creator_user.id)
        tiers = Tier.objects.filter(creator=creator_obj).values()
        patrons = get_creator_subscribers(creator_obj)
        return render(request,
                      'patron/admin/profile/creator_home.html',
                      {'creator': creator_obj,
                       'tiers': tiers,
                       'patrons': len(patrons),
                       })


@login_required
def join(request, tier_id):
    """Handles user subscription to a creator.
    Args:
        request: The incoming HTTP request object.
        tier: The tier the user wants to join
        creator: the creator the user wants to support.

    Returns:
        A rendered response with the join form and subscription status.
    """
    tier = get_tier(tier_id)
    creator = tier.creator

    if request.method == 'POST':
        patron = request.user
        TierSubscriptions.objects.get_or_create(patron=patron, tier=tier)
        messages.success(
            request, f"Welcome! You Joined my {tier.name} patrons.")
    return redirect(reverse('patron:creator_home', kwargs={"creator": creator}))


@require_POST
@login_required
def unsubscribe_patron(request, tier_id):
    """
    A view to unsubscribe a user from a tier.

    Args:
        request: The incoming HTTP request object.
        tier_id: The ID of the Tier to unsubscribe from.

    Returns:
        A redirect response to the current page after unsubscribing (or None if not subscribed).
    """
    tier = get_tier(tier_id)
    creator = tier.creator
    try:
        subscription = TierSubscriptions.objects.get(
            patron=request.user, tier__pk=tier_id)
        subscription.delete()
        messages.success(
            request, f"Successfully unsubscribed from {subscription.tier.name}")
        return redirect(reverse('patron:creator_home', kwargs={"creator": creator}))
    except TierSubscriptions.DoesNotExist:
        pass  # User not subscribed, do nothing


def list_creators(request):
    """
    Retrieves all the User's with a CreatorProfile.
    """
    creators = CreatorProfile.objects.all()
    context = {}
    context['creators'] = creators
    if request.user.is_authenticated:
        return render(request, 'patron/admin/pages/view_creators_auth.html', context)
    return render(request, 'patron/admin/pages/view_creators_unauth.html', context)


@login_required
def subscriptions(request):
    """
    Retrieves all tiers an authenticated User is subscribed to.
    """
    user_object = get_object_or_404(User, username=request.user)
    subscriptions = TierSubscriptions.objects.filter(patron=user_object)
    return render(request, 'patron/admin/pages/view_subscriptions.html', {'subscriptions': subscriptions})


@login_required
def subscription_detail(request, tier_id):
    """
    Renders a detailed view of a tier
    """
    user_object = get_object_or_404(User, username=request.user)
    tier = Tier.objects.get(pk=tier_id)
    subscription = TierSubscriptions.objects.get(tier=tier)
    return render(request, 'patron/admin/pages/view_subscription_detail.html', {'subscription': subscription, 'tier_id': tier_id})


# PAYMENT HANDLING VIEWS

@login_required
def creator_withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST)
        if form.is_valid():
            withdrawal_request = form.save(commit=False)
            # Assuming user is authenticated creator
            withdrawal_request.creator = request.user.creatorprofile
            withdrawal_request.status = 'pending'
            withdrawal_request.save()
            messages.success(
                request,
                'Withdrawal request submitted successfully. We will review your request and process it within 2 business days.')
            # Redirect to same view after successful request
            return redirect(reverse('patron:withdraw'))
    form = WithdrawalRequestForm()
    form.id = 'withdraw-form'
    total_payments = calculate_creators_balance(request.user.creatorprofile)
    pending_requests = WithdrawalRequest.objects.filter(
        creator=request.user.creatorprofile, status='pending')
    total_withdrawn = calculate_total_withdrawals(request.user.creatorprofile)
    approved_payouts = WithdrawalRequest.objects.filter(
        creator=request.user.creatorprofile, status='success')

    context = {'form': form, 'pending_requests': pending_requests, 'approved_payouts': approved_payouts,
               'total_withdrawn': total_withdrawn, 'total_payments': total_payments}
    return render(request, 'patron/admin/actions/creator_withdrawal.html', context)


@login_required
def make_payment(request, tier_id):
    """
    Makes a payment to the appropriate patrons based on (tier_sub).

    Args:
        request: The incoming HTTP request object.
        tier: The tier to make a payment for.

    Returns:
        A redirected response to the dashboard.
    """
    tier = get_tier(tier_id)
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')  # Decode bytes to string
        data = json.loads(raw_data)  # Parse JSON data
        amount = data.get('amount')
        account_number = data.get('payer_account_number')
        description = data.get('description')
        payment_method = data.get('payment_method')

        if amount and account_number:
            patron = User.objects.get(username=request.user)
            subscription = TierSubscriptions.objects.get(
                patron=patron, tier=tier)
            reference_id = generate_reference_id()

            # Create a payment object
            payment = Payments.objects.create(
                subscription=subscription, reference_id=reference_id)
            payment.amount = amount
            payment.payment_method = payment_method
            payment.payer_account_number = account_number
            payment.description = description

            # Process deposit logic here (query lipila api)
            payload = {
                'amount': amount,
                'payment_method': payment_method,
                'payer_account_number': account_number,
                'description': description
            }
            api_user = User.objects.get(pk=1)
            # process payment
            response = query_collection(
                api_user.username, 'POST', reference_id, data=payload)

            if response.status_code == 202:
                payment.status = 'accepted'
                payment.save()
                # consider making an async function
                if check_payment_status(reference_id, 'col') == 'success':
                    payment.status = 'success'
                    payment.save()
                messages.success(request, f"Paid ZMW {amount} successfully!")
                return JsonResponse({'message': 'Payment initiated successfully', 'reference_id': reference_id})
            else:
                payment.status = 'failed'
                payment.save()
                messages.error(
                    request, 'Payment failed. Please try again later!')
                return JsonResponse({'message': 'Payment failed', 'reference_id': reference_id})

        messages.error(request, f"Invalid data sent")
        form = DepositForm()
        tier = tier.name
        return render(request, 'lipila/actions/deposit.html', {'form': form, 'tier': tier})
    form = DepositForm()
    form.id = 'payment-form'
    tier = tier
    return render(request, 'lipila/actions/deposit.html', {'form': form, 'tier': tier})


# ACCOUNT HISTORY VIEWS


@login_required
def withdrawal_history(request):
    """
    This view retrives all the history of a creator's withdraw requests.
    """
    full_history = WithdrawalRequest.objects.filter(
        creator=request.user.creatorprofile)
    history = []
    context = {}
    if full_history:
        for obj in full_history:
            item = {}
            item['amount'] = obj.amount
            item['transaction_date'] = obj.request_date
            item['transaction_type'] = 'Withdraw Request'
            item['account_number'] = obj.account_number
            item['status'] = obj.status
            item['reason'] = obj.reason
            history.append(item)

    context['history'] = history
    return render(request, 'patron/admin/pages/withdrawal_history.html', context)


@login_required
def payments_history(request):
    """
    Retrieves an authenticated User's payment history.
    """
    context = {}
    try:
        creator = request.user.creatorprofile
        payments = Payments.objects.filter(subscription__tier__creator=creator)
        context['payments'] = payments
        # Retrive history for a user with a CreatorProfile
        return render(request, 'patron/admin/pages/payments_received.html', context)
    except User.creatorprofile.RelatedObjectDoesNotExist:
        # Get a patron users history
        payments = Payments.objects.filter(subscription__patron=request.user)
        context['payments'] = payments
        return render(request, 'patron/admin/pages/payments_made.html', context)


@login_required
def contributions_history(request):
    """
    Retrieves an authenticated User's payment history.
    """
    context = {}
    context = {}
    try:
        creator = request.user.creatorprofile
        contributions = Contributions.objects.filter(creator=request.user)
        context['contributions'] = contributions
        # Retrive history for a user with a CreatorProfile
        return render(request, 'patron/admin/pages/contributions_received.html', context)
    except User.creatorprofile.RelatedObjectDoesNotExist:
        # Get a patron users history
        contributions = Contributions.objects.filter(patron=request.user)
        context['contributions'] = contributions
        return render(request, 'patron/admin/pages/contributions_made.html', context)
