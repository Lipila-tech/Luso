from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as my_login
from django.contrib.auth.forms import AuthenticationForm
# My Models
from api.models import LipilaUser
from .helpers import apology
from .forms.forms import DisburseForm, AddProductForm, SignupForm, EditLipilaUserForm
from datetime import datetime
from web.models import Product
from django.urls.exceptions import NoReverseMatch

def redirect_to_lipila(request, username):
    """Redirects user to lipila.tech/<username>."""
    context = {}
    try:
        user_object = get_object_or_404(LipilaUser, username=username)
        if user_object:
            url = f"http://localhost:8000/profile/?username={username}"
            return redirect(url)
    except LipilaUser.DoesNotExist:
        return apology(request, context)


def user_profile(request, username):
    context = {}
    try:
        # username = request.GET.get('username')
        # Logic to retrieve user data based on username (e.g., from database)
        user_data = LipilaUser.objects.get(username=username)
        context['user'] = user_data
    except LipilaUser.DoesNotExist:
        context['status'] = 404
        context['message'] = f'{username} Not Found!'
        return apology(request, context, user=username)
    return render(request, 'profile/home.html', context)


# Public Views
def index(request):
    return render(request, 'UI/index.html')

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
    return render(request, 'AdminUI/pages-faq.html')


class SignupView(View):

    def get(self, request):
        form = SignupForm()
        context = {'form': form}

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
                my_login(request, user)
                return redirect(reverse('dashboard', kwargs={'user': username}))
        else:
            messages.error(
                request, "Your username and password didn't match. Please try again.")
            return redirect(reverse('login'))

    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# AUTHENTICATED USER VIEWS
class UpdateUserInfoView(View):
    def get(self, request, user, *args, **kwargs):
        user_object = get_object_or_404(LipilaUser, username=user)
        form = EditLipilaUserForm(instance=user_object)
        return render(request, 'AdminUI/profile/edit_user_info.html', {'form': form, 'user':user_object})

    def post(self, request, user, *args, **kwargs):
        user_object = get_object_or_404(LipilaUser, username=user)
        form = EditLipilaUserForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been update.")
            return redirect(reverse('profile', kwargs={'user': user_object}))
        else:
            # If form is not valid, print out the form errors for debugging
            messages.error(
                request, "Failed to update profile.")
        return render(request, 'AdminUI/profile/edit_user_info.html', {'form': form, 'user':user_object})
    
  

@login_required
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def dashboard(request, user):
    context = {}
    print('dashbord', user)
    #Dasboard  Reports 
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
        if not user:
            raise ValueError('Username missing')
        else:
            user = LipilaUser.objects.get(username=user)
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context, user=user)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context, user=user)
    except LipilaUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user=user)
    return render(request, 'AdminUI/index.html', context)


@login_required
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def profile(request, user):
    context = {}
    context['user'] = user
    print('profile',user)
    try:
        # id = int(request.GET.get('user'))
        if not user:
            raise ValueError('User ID missing')
        else:
            user = LipilaUser.objects.get(username=user)
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context, user=user)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context, user=user)
    except LipilaUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Profile Not Found!'
        print(user)
        return apology(request, context, user='auth')
    return render(request, 'AdminUI/profile/users-profile.html', context)


def bnpl(request):
    return render(request, 'AdminUI/bnpl.html')


# Logs
@login_required
def log_transfer(request):
    return render(request, 'AdminUI//log/transfer.html')


@login_required
def log_invoice(request):
    return render(request, 'AdminUI/log/invoice.html')
    

class CreateProductView(View):
    def get(self, request):
        form = AddProductForm()
        return render(request, 'AdminUI/actions/products.html', {'form': form})
    
    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save yet
            product.owner = request.user  # Set owner to current user
            product.save()
            messages.success(
                request, "Product Added Successfully.")
            return redirect(reverse('log_products'))
        else:
            messages.error(
                request, "Failed to create product.")
        return render(request, 'AdminUI/actions/products.html', {'form': form})
    

class EditProductView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)  # Fetch product by ID
        form = AddProductForm(instance=product)  # Pre-populate form with product data
        return render(request, 'AdminUI/actions/product_edit.html', {'form': form, 'product': product, 'product_id': product_id})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Product Edited Successfully.")
            return redirect('log_products')
        else:
            messages.error(
                request, "Failed to edit product.")
        return render(request, 'AdminUI/actions/product_edit.html', {'form': form, 'product': product, 'product_id': product_id})


class DeleteProductView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'AdminUI/actions/product_delete.html', {'product': product, 'product_id':product_id})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(
            request, "Product Deleted Successfully.")
        return redirect('log_products')

# Actions
@login_required
def invoice(request):
    return render(request, 'AdminUI/actions/invoice.html')


@login_required
def log_products(request):
    context = {}
    user_object = get_object_or_404(LipilaUser, username=request.user)
    products = Product.objects.filter(owner=user_object.id)
    context['products'] = products
    return render(request, 'AdminUI/log/products.html', context)


@login_required
def transfer(request):
    context = {}
    context['form'] = DisburseForm()
    return render(request, 'AdminUI//actions/transfer.html', context)
