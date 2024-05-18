from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Custom Models
from lipila.helpers import (
    apology, get_lipila_contact_info, get_user_object,
    get_lipila_index_page_info, get_testimonials, get_lipila_about_info)
from lipila.forms.forms import ContactForm
from accounts.models import CreatorProfile, PatronProfile


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
def withdraw(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    if isinstance(user_object, PatronProfile):
        return render(request, 'business/admin/actions/withdraw.html', context)
    elif isinstance(user_object, CreatorProfile):
        return render(request, 'patron/admin/actions/withdraw.html', context)
    else:
        return render(request, 'lipila/admin/actions/withdraw.html', context)

@login_required
def history(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    if isinstance(user_object, PatronProfile):
        return render(request, 'business/admin/log/withdraw.html', context)
    elif isinstance(user_object, CreatorProfile):
        return render(request, 'patron/admin/log/withdraw.html', context)
    else:
        return render(request, 'lipila/admin/log/withdraw.html', context)
