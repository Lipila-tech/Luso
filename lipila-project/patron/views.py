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
from patron.forms.forms import CreatePatronProfileForm, CreateCreatorProfileForm


def index(request):
    return render(request, 'patron/index.html')


def contribute(request, user):
    return render(request, 'patron/admin/actions/contribute.html')


@login_required
def profile(request):
    context = {}
    try:
        # Access creator profile using OneToOne relation
        creator = request.user.creatorprofile
    except CreatorProfile.DoesNotExist:
        pass
    try:
        patron = request.user.patronprofile
    except PatronProfile.DoesNotExist:
        messages.info(
            request, 'Please Choose your profile type.')
        return redirect('choose_profile_type')
    context['user'] = get_user_object(request.user)
    print(patron)
    print(request.user)
    return render(request, 'patron/admin/profile/users-profile.html', context)


@login_required
def create_creator_profile(request):
    creator = get_user_object(request.user)
    if request.method == 'POST':
        print('post received')
        print('creating form')
        form = CreateCreatorProfileForm(
            request.POST)
        print('form created')
        if form.is_valid():
            print('form is valid')
            creator_profile = form.save(commit=False)  # Don't save yet
            creator_profile.user = creator  # Set the user based on the logged-in user
            creator_profile.save()
            messages.success(
                request, "Your profile data has been saved.")
            return redirect(reverse('profile'))
        else:
            print('invalid form')
            print(form)
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
            # Redirect to creator profile creation view (replace with your URL name)
            return redirect('create_creator_profile')
        elif profile_type == 'patron':
            # Redirect to patron profile creation view (replace with your URL name)
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

    # Recent activities
    context['activities'] = [
        ('Last login', last_login_time),
        ('Receipts', 150),
        ('Pay Outs', 100),
        ('Sent Invoices', 5),
    ]
    user_object = get_user_object(user)

    if isinstance(user_object, User):
        user_object = User.objects.get(username=user)
        context['user'] = user_object
        return render(request, 'patron/admin/index.html', context)
    else:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user=user)


def patron(request):
    context = {}
    patron = CreatorProfile.objects.all()
    # user_object = get_user_object(user)
    context['patron'] = patron
    if request.user.is_authenticated:
        # context['user'] = user_object
        return render(request, 'lipila/admin/patron.html', context)
    else:
        return render(request, 'UI/patron.html', context)


@login_required
def join(request, creator, user):
    """Handles user subscription to a creator.

    Args:
        request: The incoming HTTP request object.
        creator: The username of the creator the user wants to join.

    Returns:
        A rendered response with the join form and subscription status.
    """
    pass


def list_creators(request):
    data = [
        {
            'username': 'SampleUsername',
            'bio': 'This is a sample creator bio',
            'created_at': '2024-06-01'
        },
        {
            'username': 'SampleCreator2',
            'bio': 'This is a sample creator number 2 bio',
            'created_at': '2024-06-01'
        },
        {
            'username': 'SampleCreator3',
            'bio': 'This is a sample creator number 3 bio',
            'created_at': '2024-06-01'
        }
    ]
    context = {}
    context['creators'] = data
    return render(request, 'patron/creators.html', context)


@login_required
def log_products(request, user):
    context = {}
    user_object = get_object_or_404(CreatorProfile, username=request.user)
    products = Product.objects.filter(owner=user_object.id)
    context['products'] = products
    context['user'] = user_object
    return render(request, 'patron/admin/log/products.html', context)
