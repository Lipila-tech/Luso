from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# custom modules
from accounts.models import CreatorProfile, PatronProfile
from business.models import Product
from lipila.helpers import get_user_object, apology
from patron.forms.forms import (
    CreatePatronProfileForm, CreateCreatorProfileForm, EditTiersForm,
    DepositForm, ContributeForm)
from patron.models import Tier, TierSubscriptions, Payments
from patron.helpers import get_creator_subscribers, get_creator_url, get_tier



def index(request):
    """
    Renders the Lipila Patron home page.
    """
    return render(request, 'patron/index.html')

@login_required
def withdraw(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    return render(request, 'patron/admin/actions/withdraw.html', context)


@login_required
def profile(request):
    context = {}
    if request.user.is_staff:
        return redirect(reverse('staff_dashboard', kwargs={'user': request.user}))
    try:
        # Access creator profile using OneToOne relation
        patron = request.user.patronprofile
        context['user'] = get_user_object(patron)
        return render(request, 'patron/admin/profile/users-profile.html', context)
    except PatronProfile.DoesNotExist:
        pass
    try:
        creator = request.user.creatorprofile
        context['user'] = get_user_object(creator)
        return render(request, 'patron/admin/profile/users-profile.html', context)
    except CreatorProfile.DoesNotExist:
        messages.info(
            request, 'Please Choose your profile type.')
        return redirect('choose_profile_type')


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
            return redirect(reverse('profile'))
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
            return redirect(reverse('profile'))
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
            return redirect('create_creator_profile')
        elif profile_type == 'patron':
            return redirect('create_patron_profile')
        else:
            messages.error(request, 'Invalid profile type selected.')
    return render(request, 'patron/admin/profile/choose_profile_type.html')


class EditUserProfile(LoginRequiredMixin, View):
    def get(self, request, user, *args, **kwargs):
        try:
            # Access creator profile using OneToOne relation
            creator = request.user.creatorprofile
        except CreatorProfile.DoesNotExist:
            messages.info(
                request, 'Please Choose your profile type.')
            # Redirect to profile creation view
            return redirect('choose_profile_type')
        form = CreateCreatorProfileForm(instance=creator)
        return render(request,
                      'patron/admin/profile/edit_user_info.html',
                      {'form': form, 'user': creator})

    def post(self, request, user, *args, **kwargs):
        try:
            # Access creator profile using OneToOne relation
            creator = request.user.creatorprofile
        except CreatorProfile.DoesNotExist:
            messages.info(
                request, 'Please Choose your profile type.')
            # Redirect to profile creation view
            return redirect('choose_profile_type')
        form = CreateCreatorProfileForm(
            request.POST, request.FILES, instance=creator)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated.")
            return redirect(reverse('profile'))
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('profile'))


@login_required
def staff_users(request, user):
    all_users = User.objects.all().order_by('date_joined')
    all_creators = CreatorProfile.objects.all()
    total_payments = 1000
    return render(request, 'lipila/staff/users.html', {
        'all_users': len(all_users),
        'all_creators': len(all_creators),
        'total_payments': total_payments,
        'updated_at': datetime.today
    })


def contribute(request, creator):
    if request.method == 'POST':
        form = ContributeForm(request.POST)
    form = ContributeForm()
    return render(request, 'lipila/actions/contribute.html', {'form':form, 'tier':'One-time contribution'})

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
        form = DepositForm(request.POST)
        if form.is_valid():
            patron = User.objects.get(username=request.user)
            subscription = TierSubscriptions.objects.get(
                patron=patron, tier=tier)
            # Process deposit logic here (e.g., connect to payment gateway, store transaction details)
            amount = form.cleaned_data['amount']
            phone_number = form.cleaned_data['phone_number']
            payment = Payments.objects.create(
                subscription=subscription, amount=amount)
            payment.save()
            messages.success(request, f"Paid ZMW {amount} successfully!")
            # Redirect to user dashboard after successful deposit
            return redirect(reverse('dashboard', kwargs={'user': request.user}))
    form = DepositForm()
    tier = tier.name
    return render(request, 'lipila/actions/deposit.html', {'form': form, 'tier': tier})


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

    context = {}
    now = datetime.now()
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
            'updated_at': datetime.today
        }
        patron = request.user.patronprofile
        context['user'] = get_user_object(patron)
        return render(request, 'patron/admin/index_patron.html', context)
    except PatronProfile.DoesNotExist:
        pass
    try:
        # Creator summary
        context['summary'] = {
            'balance': 2500,
            'withdraws': 45000,
            'patrons': 100,
            'tiers': 3,
            'updated_at': datetime.today
        }
        creator = request.user.creatorprofile
        url = get_creator_url('index', creator, domain='localhost:8000')
        context['user'] = get_user_object(creator)
        context['url'] = url
        return render(request, 'patron/admin/index_creator.html', context)
    except CreatorProfile.DoesNotExist:
        messages.info(
            request, 'Please Choose your profile type.')
        return redirect('choose_profile_type')


@login_required
def patron(request):
    """
    Retrives a users patrons.
    """
    context = {}
    creator = get_object_or_404(CreatorProfile, user=request.user)
    patrons = get_creator_subscribers(creator)
    context['patrons'] = patrons
    return render(request, 'patron/admin/pages/patrons.html', context)


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
                       'patrons':len(patrons),
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
                       'patrons':len(patrons),
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
        return render(request, 'patron/admin/pages/creators.html', context)
    return render(request, 'patron/creators.html', context)


@login_required
def subscriptions(request):
    """
    Retrieves all tiers an authenticated User is subscribed to.
    """
    user_object = get_object_or_404(User, username=request.user)
    subscriptions = TierSubscriptions.objects.filter(patron=user_object)
    return render(request, 'patron/admin/pages/subscriptions.html', {'subscriptions':subscriptions})


@login_required
def history(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    return render(request, 'patron/admin/pages/history.html', context)


@login_required
def payments(request):
    """
    Retrieves an authenticated User's payment history.
    """
    context = {}
    user = get_user_object(request.user)
    context['user'] = user
    tiers = TierSubscriptions.objects.filter(patron=user)
    print(tiers)
    for tier in tiers:
        print(tier.payments)
    payments = Payments.objects.filter(subscription=tier)
    print(payments)
    context['payments'] = payments

    return render(request, 'patron/admin/pages/payments.html', context)
