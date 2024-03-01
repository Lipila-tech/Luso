from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.views import View
from django.contrib import messages

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

def pages_faq(request):
    return render(request, 'AdminUI/pages-faq.html')

# Auth
class SignupView(View):
    
    def get(self, request):
        form = SignupForm()
        context = {'form': form}
        
        return render(request, 'Auth/signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST)
        context = {'form': form}

        try:
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS,
                                    "Account created successfully")
                return redirect('login')
            else:
                messages.add_message(request, messages.ERROR, "Error during signup!")
                return render(request, 'Auth/signup.html', context)
        except Exception as e:
            print(e)

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

def bnpl(request):
    return render(request, 'AdminUI/bnpl.html')

# Logs
def log_transfer(request):
    return render(request, 'AdminUI//log/transfer.html')

def log_invoice(request):
    return render(request, 'AdminUI/log/invoice.html')

def log_products(request):
    return render(request, 'AdminUI/log/products.html')

# Actions
def invoice(request):
    return render(request, 'AdminUI/actions/invoice.html')

def products(request):
    return render(request, 'AdminUI/actions/products.html')

def transfer(request):
    context = {}
    context['form'] = DisburseForm()
    return render(request, 'AdminUI//actions/transfer.html', context)