from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from datetime import datetime
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
# custom modules
from accounts.models import CreatorProfile, PatronProfile
from business.models import Product
from lipila.helpers import get_user_object, apology
from patron.forms.forms import EditPatronProfileForm, EditCreatorProfileForm


def index(request):
    return render(request, 'patron/index.html')

def contribute(request, user):
    return render(request, 'patron/admin/actions/contribute.html')

@login_required
def profile(request):
    user = request.user
    context = {}
    user_object = get_user_object(user)
    if isinstance(user_object, User):
        context['user'] = user_object
        return render(request, 'patron/admin/profile/users-profile.html', context)
    else:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user='auth')


class EditUserProfile(LoginRequiredMixin, View):
    def get(self, request, user, *args, **kwargs):
        user_object = get_user_object(user)
        if isinstance(user_object, User):
            form = EditCreatorProfileForm(instance=user_object)
            return render(request,
                          'patron/admin/profile/edit_user_info.html',
                          {'form': form, 'user': user_object})
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('profile', kwargs={'user': user}))

    def post(self, request, user, *args, **kwargs):
        user_object = get_user_object(user)
        if isinstance(user_object, User):
            form = EditCreatorProfileForm(
                request.POST, request.FILES, instance=user_object)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your profile has been update.")
                return redirect(reverse('profile', kwargs={'user': user_object}))
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('profile', kwargs={'user': user}))

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


@login_required
def list_patrons(request, user):
    context = {}
    user_object = get_object_or_404(CreatorProfile, username=request.user)
    patrons = PatronProfile.objects.filter(patron=user_object.id)
    context['patrons'] = patrons
    context['user'] = user_object
    return render(request, 'patron/admin/log/patrons.html', context)


@login_required
def log_products(request, user):
    context = {}
    user_object = get_object_or_404(CreatorProfile, username=request.user)
    products = Product.objects.filter(owner=user_object.id)
    context['products'] = products
    context['user'] = user_object
    return render(request, 'patron/admin/log/products.html', context)