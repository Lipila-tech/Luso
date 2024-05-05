from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, renderer_classes
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from datetime import datetime
# Custom Models
from lipila.helpers import (
    apology, get_lipila_contact_info, get_user_object, check_if_user_is_patron,
    get_lipila_index_page_info, get_testimonials, get_lipila_about_info)
from lipila.models import ContactInfo
from lipila.forms.forms import ContactForm
from patron.models import CreatorUser, Patron


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

def patron(request):
    context = {}
    patron = CreatorUser.objects.all()
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
                if patron.patron.filter(pk=creator_object.pk).exists():
                    
                    messages.info(request, f"You're already subscribed to {creator_object.user}.")
                else:
                    # Subscribe to creator
                    patron.patron.add(creator_object)
                    
                    messages.success(request, f"Subscribed to {creator_object.username}")
            else:
                patron.save()  # Save additional Patron details if applicable
                
                messages.success(request, f"Subscribed to {creator_object.username}")

            return redirect('patron')
    patron_exists = check_if_user_is_patron(user_obj, creator_object)
    
    
    context = {
        'join_form': form,
        'creator': creator_object,
        'is_patron': patron_exists,
        'user':user_obj
    }

    return render(request, 'lipila/admin/join.html', context)

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
    return render(request, 'UI/index.html', context)

@login_required
def withdraw(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    if isinstance(user_object, Patron):
        return render(request, 'business/admin/actions/withdraw.html', context)
    elif isinstance(user_object, CreatorUser):
        return render(request, 'patron/admin/actions/withdraw.html', context)
    else:
        return render(request, 'lipila/admin/actions/withdraw.html', context)


@login_required
def history(request, user):
    context = {}
    user_object = get_user_object(request.user)
    context['user'] = user_object
    if isinstance(user_object, Patron):
        return render(request, 'business/admin/log/withdraw.html', context)
    elif isinstance(user_object, CreatorUser):
        return render(request, 'patron/admin/log/withdraw.html', context)
    else:
        return render(request, 'lipila/admin/log/withdraw.html', context)
