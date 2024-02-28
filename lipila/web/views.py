from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# My Models
from api.models import MyUser
from .helpers import apology
from .forms.forms import DisburseForm, LoginForm, SignupForm


# Public Views
def index(request):
    return render(request, 'UI/index.html')

def service_details(request):
    return render(request, 'UI/services-details.html')

def portfolio_details(request):
    return render(request, 'UI/portfolio-details.html')

def send_money(request):
    form = request.GET
    if form:
        payee_id =  form['payee_id']
        try:
            data = MyUser.objects.get(username=payee_id)
            context = {}
            context['payee'] = data.username
            context['location'] = data.city
        except MyUser.DoesNotExist:
            context = {'message': "User id not found",}
            return render(request, '404.html', context)
        
    return render(request, 'UI/send_money.html', context)


def disburse(request):
    """View for the page homapage"""
    context = {}
    context['form'] = DisburseForm()
    return render(request, 'disburse.html', context)

def pages_faq(request):
    return render(request, 'AdminUI/pages-faq.html')

def signup(request):
    context = {}
    context['form'] = SignupForm()
    return render(request, 'Auth/signup.html', context)

def login(request):
    context = {}
    context['form'] = LoginForm()
    return render(request, 'Auth/login.html', context)


# Authenticated User Views
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def dashboard(request, id):
    context = {}
    try:
        # id = int(request.GET.get('user'))
        if not id:
            raise ValueError('User ID missing')
        else:
            user = MyUser.objects.get(id=int(id))
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context)
    except MyUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context)
    return render(request, 'AdminUI/index.html', context)


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def users_profile(request, id):
    context = {}
    try:
        # id = int(request.GET.get('user'))
        if not id:
            raise ValueError('User ID missing')
        else:
            user = MyUser.objects.get(id=int(id))
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context)
    except MyUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Profile Not Found!'
        return apology(request, context)
    return render(request, 'AdminUI/users-profile.html', context)

def logout(request):
    pass

def history(request):
    return render(request, 'AdminUI/history.html')

def bnpl(request):
    return render(request, 'AdminUI/bnpl.html')

def sales(request):
    return render(request, 'AdminUI/sales.html')
