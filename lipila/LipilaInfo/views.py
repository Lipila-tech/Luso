from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as my_login
from django.contrib.auth.forms import AuthenticationForm
# My Models
from LipilaInfo.helpers import apology, get_lipila_contact_info
from LipilaInfo.models import ContactInfo, LipilaUser
from LipilaInfo.forms.forms import ContactForm, SignupForm, EditLipilaUserForm
from business.forms.forms import EditBusinessUserForm
from creators.forms.forms import EditCreatorUserForm
from business.models import BusinessUser, Student
from creators.models import CreatorUser
from datetime import datetime
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


# Public Views
def index(request):
    form = ContactForm()
    context = get_lipila_contact_info()
    context['form'] = form

    return render(request, 'UI/index.html', context)


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
    return render(request, 'disburse/pages-faq.html')


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
                    my_login(request, user)
                    return redirect(reverse('dashboard', kwargs={'user': username}))
                except BusinessUser.DoesNotExist:
                    pass  # Continue to next check
                try:
                    user_object = CreatorUser.objects.get(username=user)
                    my_login(request, user)
                    return redirect(reverse('dashboard', kwargs={'user': username}))
                except CreatorUser.DoesNotExist:
                    pass  # Continue to next check
                try:
                    user_object = LipilaUser.objects.get(username=user)
                    my_login(request, user)
                    return redirect(reverse('dashboard', kwargs={'user': username}))
                except LipilaUser.DoesNotExist:
                    messages.error(request, "Invalid username or password.")
                    # Redirect to login with error message
                    return redirect('login')
        else:
            messages.error(
                request, "Your username and password didn't match. Please try again.")
            return redirect(reverse('login'))

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
    context['user'] = user
    try:
        user_object = BusinessUser.objects.get(username=user)
        context['user'] = user_object
        return render(request, 'business/admin/profile/users-profile.html', context)
    except BusinessUser.DoesNotExist:
        pass  # Continue to next check
    try:
        user_object = CreatorUser.objects.get(username=user)
        context['user'] = user_object
        return render(request, 'creators/admin/profile/users-profile.html', context)
    except CreatorUser.DoesNotExist:
        pass  # Continue to next check
    try:
        user_object = LipilaUser.objects.get(username=user)
        context['user'] = user_object
        return render(request, 'disburse/profile/users-profile.html', context)
    except LipilaUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user='auth')


# AUTHENTICATED USER VIEWS
class UpdateUserInfoView(View):
    def get(self, request, user, *args, **kwargs):
        try:
            user_object = BusinessUser.objects.get(username=user)
            form = EditBusinessUserForm(instance=user_object)
            return render(request, 'business/admin//profile/edit_user_info.html', {'form': form, 'user': user_object})
        except BusinessUser.DoesNotExist:
            pass  # Continue to next check
        try:
            user_object = CreatorUser.objects.get(username=user)
            form = EditCreatorUserForm(instance=user_object)
            return render(request, 'creators/admin/profile/edit_user_info.html', {'form': form, 'user': user_object})
        except CreatorUser.DoesNotExist:
            pass  # Continue to next check
        try:
            user_object = LipilaUser.objects.get(username=user)
            form = EditLipilaUserForm(instance=user_object)
            return render(request, 'disburse/profile/edit_user_info.html', {'form': form, 'user': user_object})
        except LipilaUser.DoesNotExist:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('profile', kwargs={'user': user}))
        

    def post(self, request, user, *args, **kwargs):
        try:
            user_object = BusinessUser.objects.get(username=user)
            form = EditLipilaUserForm(
                request.POST, request.FILES, instance=user_object)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your profile has been update.")
                return redirect(reverse('profile', kwargs={'user': user_object}))
        except BusinessUser.DoesNotExist:
            pass  # Continue to next check
        try:
            user_object = CreatorUser.objects.get(username=user)
            form = EditLipilaUserForm(
                request.POST, request.FILES, instance=user_object)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your profile has been update.")
                return redirect(reverse('profile', kwargs={'user': user_object}))
        except CreatorUser.DoesNotExist:
            pass  # Continue to next check
        try:
            user_object = LipilaUser.objects.get(username=user)
            form = EditLipilaUserForm(
                request.POST, request.FILES, instance=user_object)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your profile has been update.")
                return redirect(reverse('profile', kwargs={'user': user_object}))
        except LipilaUser.DoesNotExist:
            messages.error(
                request, "Failed to update profile.")
            return redirect(reverse('profile', kwargs={'user': user}))


@login_required
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def dashboard(request, user):
    context = {}
    # Dasboard  Reports
    context['sales'] = 0
    context['sales_increase'] = 0
    context['revenue'] = 0
    context['increase'] = 0
    context['customers'] = 0

    # Top selling
    context['topselling'] = [
        (1245, 'product1', 199,  200, 3599),
        (1233, 'product2', 199,  200, 3599),
        (2345, 'product3', 199,  200, 3599),
        (2345, 'product4', 199,  200, 3599),
        (3333, 'product5', 199,  200, 3599),
        (4355, 'product6', 199,  200, 3599),
    ]

    # Recent sales
    context['recentsales'] = [
        ('12/03/24', 'customer1', 'product123',  343, 'Approved'),
        ('12/03/24', 'customer2', 'product123',  200, 'Approved'),
        ('12/03/24', 'customer3', 'product123',  240, 'Approved'),
        ('12/03/24', 'customer4', 'product123',  200, 'Approved'),
        ('12/03/24', 'customer5', 'product123',  200, 'Approved'),
        ('12/03/24', 'customer6', 'product123',  200, 'Approved'),
    ]

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
    try:
        context = {}
        user_object = BusinessUser.objects.get(username=user)
        students = Student.objects.filter(school=user_object.id)
        context['students'] = students.count()
        context['user'] = user_object
        return render(request, 'business/admin/index.html', context)
    except BusinessUser.DoesNotExist:
        pass  # Continue to next check
    try:
        user_object = CreatorUser.objects.get(username=user)
        context['user'] = user_object
        return render(request, 'creators/admin/index.html', context)
    except CreatorUser.DoesNotExist:
        pass  # Continue to next check
    try:
        user_object = LipilaUser.objects.get(username=user)
        context['user'] = user_object
        return render(request, 'disburse/index.html', context)
    except LipilaUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user=user)
