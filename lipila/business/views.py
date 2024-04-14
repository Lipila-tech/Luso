from django.urls import reverse
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
from api.models import BusinessUser
from .helpers import apology
from .forms.forms import DisburseForm, AddProductForm, SignupForm, EditBusinessUserForm
from datetime import datetime
from business.models import Product


def index(request):
    return render(request, 'business/index.html')



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

class SignupView(View):

    def get(self, request):
        form = SignupForm()
        context = {'form': form, 'category': 'Business'}
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
