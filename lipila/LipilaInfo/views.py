from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, renderer_classes
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as my_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from datetime import datetime
# Custom Models
from LipilaInfo.helpers import (
    apology, get_lipila_contact_info, get_user_object, check_if_user_is_patron,
    get_lipila_home_page_info, get_testimonials, get_lipila_about_info)
from LipilaInfo.models import ContactInfo, LipilaUser
from LipilaInfo.forms.forms import ContactForm, SignupForm, EditLipilaUserForm
from business.forms.forms import EditBusinessUserForm
from creators.forms.forms import EditCreatorUserForm
from business.models import BusinessUser, Student
from creators.models import CreatorUser, Patron


# Public Views
def index(request):
    context = {}
    form = ContactForm()
    contact_info = get_lipila_contact_info()
    lipila_home = get_lipila_home_page_info()
    testimonial = get_testimonials()
    about = get_lipila_about_info()
    context['form'] = form
    context['contact'] = contact_info['contact']
    context['lipila'] = lipila_home['lipila']
    context['about'] = about['about']
    context['testimony'] = testimonial

    return render(request, 'UI/index.html', context)


def creators(request):
    context = {}
    creators = CreatorUser.objects.all()
    # user_object = get_user_object(user)
    context['creators'] = creators
    if request.user.is_authenticated:
        # context['user'] = user_object
        return render(request, 'LipilaInfo/admin/creators.html', context)
    else:
        return render(request, 'UI/creators.html', context)


@login_required
def join(request, creator, user):
    """Handles user subscription to a creator.

    Args:
        request: The incoming HTTP request object.
        creator: The username of the creator the user wants to join.

    Returns:
        A rendered response with the join form and subscription status.
    """
    form = 'JoinForm()'
    context = {}
    creator_object = CreatorUser.objects.get(username=creator)
    user_obj = get_user_object(user)

    if request.method == 'POST':
        form = 'JoinForm(request.POST)'
        if form.is_valid():
            patron, created = Patron.objects.get_or_create(user=user_obj)  # Get or create Patron
            
            if not created:  # User already a Patron
                # Check if already subscribed (implement logic based on your model fields)
                if patron.creators.filter(pk=creator_object.pk).exists():
                    
                    messages.info(request, f"You're already subscribed to {creator_object.user}.")
                else:
                    # Subscribe to creator
                    patron.creators.add(creator_object)
                    
                    messages.success(request, f"Subscribed to {creator_object.username}")
            else:
                patron.save()  # Save additional Patron details if applicable
                
                messages.success(request, f"Subscribed to {creator_object.username}")

            return redirect('creators')
    patron_exists = check_if_user_is_patron(user_obj, creator_object)
    
    
    context = {
        'join_form': form,
        'creator': creator_object,
        'is_patron': patron_exists,
        'user':user_obj
    }

    return render(request, 'LipilaInfo/admin/join.html', context)



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
            data = LipilaUser.objects.get(username=payee_id)
            context['payee'] = payee_id
            context['location'] = data.city
        except LipilaUser.DoesNotExist:
            context = {'message': "User id not found", }
            return render(request, '404.html', context)

    return render(request, 'UI/send_money.html', context)


def pages_faq(request):
    return render(request, 'LipilaInfo/pages/pages_faq.html')

def pages_terms(request):
    return render(request, 'LipilaInfo/pages/pages_terms.html')

def pages_privacy(request):
    return render(request, 'LipilaInfo/pages/pages_privacy.html')


class SignupView(View):

    def get(self, request):
        form = SignupForm()
        context = {'form': form, 'category': 'Consumer'}

        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST)
        context = {'form': form}

        try:
            if form.is_valid():
                user = form.save(commit=False)  # Don't save directly
                user.set_password(user.password)
                user.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Account created successfully")
                return redirect('login')
            else:
                messages.add_message(
                    request, messages.ERROR, "Error during signup!")
                return render(request, 'registration/signup.html', context)
        except Exception as e:
            messages.add_message(
                request, messages.ERROR, "Error during signup!")
            return render(request, 'registration/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                try:
                    user_object = BusinessUser.objects.get(username=user)
                    my_login(request, user_object)
                    return redirect(reverse('dashboard', kwargs={'user': username}))
                except BusinessUser.DoesNotExist:
                    pass  # Continue to next check
                try:
                    user_object = CreatorUser.objects.get(username=user)
                    my_login(request, user_object)

                    return redirect(reverse('dashboard', kwargs={'user': username}))
                except CreatorUser.DoesNotExist:
                    pass  # Continue to next check
                try:
                    user_object = LipilaUser.objects.get(username=user)
                    my_login(request, user_object)
                    messages.success(request, "Logged in")
                    return redirect(reverse('dashboard', kwargs={'user': username}))
                except LipilaUser.DoesNotExist:
                    messages.error(request, "Invalid username or password.")
                    return redirect('login')
        else:
            form = AuthenticationForm()
            messages.error(request, "Your username and password didn't match")
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


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
    return render(request, 'UI/index.html', context)


@login_required
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def profile(request, user):
    context = {}
    user_object = get_user_object(user)
    if isinstance(user_object, BusinessUser):
        context['user'] = user_object
        return render(request, 'business/admin/profile/users-profile.html', context)
    elif isinstance(user_object, CreatorUser):
        context['user'] = user_object
        return render(request, 'creators/admin/profile/users-profile.html', context)
    elif isinstance(user_object, LipilaUser):
        context['user'] = user_object
        return render(request, 'LipilaInfo/admin/profile/users-profile.html', context)
    else:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user='auth')


# AUTHENTICATED USER VIEWS
class UpdateUserInfoView(View):
    def get(self, request, user, *args, **kwargs):
        user_object = get_user_object(user)
        if isinstance(user_object, BusinessUser):
            form = EditBusinessUserForm(instance=user_object)
            return render(request,
                          'business/admin//profile/edit_user_info.html',
                          {'form': form, 'user': user_object})
        elif isinstance(user_object, CreatorUser):
            form = EditCreatorUserForm(instance=user_object)
            return render(request,
                          'creators/admin/profile/edit_user_info.html',
                          {'form': form, 'user': user_object})
        elif isinstance(user_object, LipilaUser):
            form = EditLipilaUserForm(instance=user_object)
            return render(request,
                          'LipilaInfo/admin/profile/edit_user_info.html',
                          {'form': form, 'user': user_object})
        else:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('profile', kwargs={'user': user}))

    def post(self, request, user, *args, **kwargs):
        user_object = get_user_object(user)
        if isinstance(user_object, BusinessUser):
            form = EditBusinessUserForm(
                request.POST, request.FILES, instance=user_object)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your profile has been update.")
                return redirect(reverse('profile', kwargs={'user': user_object}))
        elif isinstance(user_object, CreatorUser):
            form = EditCreatorUserForm(
                request.POST, request.FILES, instance=user_object)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your profile has been update.")
                return redirect(reverse('profile', kwargs={'user': user_object}))
        elif isinstance(user_object, LipilaUser):
            form = EditLipilaUserForm(
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
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
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

    if isinstance(user_object, BusinessUser):
        students = Student.objects.filter(school=user_object.id)
        context['students'] = students.count()
        context['user'] = user_object
        return render(request, 'business/admin/index.html', context)
    elif isinstance(user_object, CreatorUser):
        user_object = CreatorUser.objects.get(username=user)
        context['user'] = user_object
        # context['patrons'] = user_objects[1]
        return render(request, 'creators/admin/index.html', context)
    elif isinstance(user_object, LipilaUser):
        user_object = LipilaUser.objects.get(username=user)
        context['user'] = user_object
        # context['patrons'] = user_objects[1]
        return render(request, 'LipilaInfo/admin/index.html', context)
    else:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user=user)


@login_required
def withdraw(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    if isinstance(user_object, BusinessUser):
        return render(request, 'business/admin/actions/withdraw.html', context)
    elif isinstance(user_object, CreatorUser):
        return render(request, 'creators/admin/actions/withdraw.html', context)
    else:
        return render(request, 'LipilaInfo/admin/actions/withdraw.html', context)


@login_required
def history(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    if isinstance(user_object, BusinessUser):
        return render(request, 'business/admin/log/withdraw.html', context)
    elif isinstance(user_object, CreatorUser):
        return render(request, 'creators/admin/log/withdraw.html', context)
    else:
        return render(request, 'LipilaInfo/admin/log/withdraw.html', context)
