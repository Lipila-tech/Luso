from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from datetime import datetime
from django.contrib.auth.decorators import login_required
# custom modules
from accounts.models import CreatorProfile, PatronProfile
from business.models import Product
from lipila.helpers import get_user_object, apology
from patron.forms.forms import CreatePatronProfileForm, CreateCreatorProfileForm, EditTiersForm
from patron.models import Tier


def index(request):
    return render(request, 'patron/index.html')


def contribute(request, user):
    return render(request, 'patron/admin/actions/contribute.html')


@login_required
def withdraw(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    return render(request, 'patron/admin/actions/withdraw.html', context)


@login_required
def profile(request):
    context = {}
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
def dashboard(request, user):
    context = {}
    now = datetime.now()
    request.session['last_login_time'] = now.strftime("%H:%M:%S")
    last_login_time = request.session.get('last_login_time')
    if last_login_time:
        context['last_login'] = last_login_time
    user_object = get_user_object(user)
    try:
        # patron summary
        context['summary'] = {
            'subscriptions': 30,
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
        context['user'] = get_user_object(creator)
        return render(request, 'patron/admin/index_creator.html', context)
    except CreatorProfile.DoesNotExist:
        messages.info(
            request, 'Please Choose your profile type.')
        return redirect('choose_profile_type')


def patron(request):
    context = {}
    patron = CreatorProfile.objects.all()
    patrons = [
        {'name': 'user1', 'city': 'Kitwe',
            'subscription': 'Gold', 'contributions': 1200},
        {
            'name': 'user2', 'city': 'Lusaka', 'subscription': 'Gold', 'contributions': 300},
        {'name': 'user3', 'city': 'Ndola', 'subscription': 'Silver', 'contributions': 300}]
    context['patrons'] = patrons
    if request.user.is_authenticated:
        return render(request, 'patron/admin/pages/patrons.html', context)
    else:
        return render(request, 'UI/patron.html', context)


def view_tiers(request):
    """
    renders a creators tiers.
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
    creator_id = User.objects.get(username=creator)
    creator_obj = CreatorProfile.objects.get(user=creator_id)
    return render(request, 'patron/admin/profile/creator_home.html', {'creator': creator_obj})


# @login_required
def join(request, tier_id):
    """Handles user subscription to a creator.
    Args:
        request: The incoming HTTP request object.
        tier: The tier the user wants to join
        creator: the creator the user wants to support.

    Returns:
        A rendered response with the join form and subscription status.
    """
    creator_obj = User.objects.get(username=tier_id)
    print('creator', creator_obj.creatorprofile.patron_title)
    messages.success(
        request, f'Congratulations! You Joined {tier_id} susbcription.')
    return redirect(reverse('creator_home', kwargs={'creator': tier_id}))


def list_creators(request):
    creators = CreatorProfile.objects.all()
    context = {}
    context['creators'] = creators
    return render(request, 'patron/creators.html', context)


@login_required
def log_products(request, user):
    context = {}
    user_object = get_object_or_404(CreatorProfile, username=request.user)
    products = Product.objects.filter(owner=user_object.id)
    context['products'] = products
    context['user'] = user_object
    return render(request, 'patron/admin/log/products.html', context)


@login_required
def history(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    return render(request, 'patron/admin/pages/history.html', context)
