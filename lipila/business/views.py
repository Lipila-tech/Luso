from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
# My Models
from api.models import BusinessUser
from .helpers import apology
from .forms.forms import DisburseForm, AddProductForm, SignupForm, EditBusinessUserForm
from datetime import datetime
from business.models import Product


def index(request):
    return render(request, 'business/index.html')

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
            user = BusinessUser.objects.get(username=user)
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context, user=user)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context, user=user)
    except BusinessUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context, user=user)
    return render(request, 'business/admin/index.html', context)


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
            user = BusinessUser.objects.get(username=user)
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context, user=user)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context, user=user)
    except BusinessUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Profile Not Found!'
        print(user)
        return apology(request, context, user='auth')
    return render(request, 'business/admin/profile/users-profile.html', context)


def bnpl(request):
    return render(request, 'business/admin/bnpl.html')


# Logs
@login_required
def log_transfer(request):
    return render(request, 'business/admin//log/transfer.html')


@login_required
def log_invoice(request):
    return render(request, 'business/admin/log/invoice.html')
    

class CreateProductView(View):
    def get(self, request):
        form = AddProductForm()
        return render(request, 'business/admin/actions/products.html', {'form': form})
    
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
        return render(request, 'business/admin/actions/products.html', {'form': form})
    

class EditProductView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)  # Fetch product by ID
        form = AddProductForm(instance=product)  # Pre-populate form with product data
        return render(request, 'business/admin/actions/product_edit.html', {'form': form, 'product': product, 'product_id': product_id})

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
        return render(request, 'business/admin/actions/product_edit.html', {'form': form, 'product': product, 'product_id': product_id})


class DeleteProductView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'business/admin/actions/product_delete.html', {'product': product, 'product_id':product_id})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(
            request, "Product Deleted Successfully.")
        return redirect('log_products')

# Actions
@login_required
def invoice(request):
    return render(request, 'business/admin/actions/invoice.html')


@login_required
def log_products(request):
    context = {}
    user_object = get_object_or_404(BusinessUser, username=request.user)
    products = Product.objects.filter(owner=user_object.id)
    context['products'] = products
    return render(request, 'business/admin/log/products.html', context)


@login_required
def transfer(request):
    context = {}
    context['form'] = DisburseForm()
    return render(request, 'business/admin//actions/transfer.html', context)
