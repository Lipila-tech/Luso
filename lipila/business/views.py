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
from LipilaInfo.helpers import apology, get_user_object
from .forms.forms import (DisburseForm, AddProductForm,
                          SignupForm, EditBusinessUserForm,
                          AddStudentForm)
from datetime import datetime
from business.models import Product, Student
from patron.models import CreatorUser


def index(request):
    return render(request, 'business/index.html')


class CreateStudentView(View):
    def get(self, request):
        form = AddStudentForm()
        return render(request, 'business/admin/actions/students.html', {'form': form})

    def post(self, request):
        user_object = get_object_or_404(BusinessUser, username=request.user)
        school = user_object  # Assign the user's BusinessUser object to school

        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)  # Don't save yet
            student.school = school  # Set the school based on the logged-in user
            student.save()
            messages.success(
                request, "Student Added Successfully.")
            return redirect(reverse('business:list_student'))
        else:
            messages.error(
                request, "Failed to create Student.")
        return render(request, 'business/admin/actions/students.html', {'form': form})


class EditStudentView(View):
    def get(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(
            Student, pk=student_id)  # Fetch student by ID
        # Pre-populate form with student data
        form = AddStudentForm(instance=student)
        return render(request,
                      'business/admin/actions/student_edit.html',
                      {'form': form, 'student': student, 'student_id': student_id})

    def post(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, pk=student_id)
        form = AddStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Student Edited Successfully.")
            return redirect('business:list_student')
        else:
            messages.error(
                request, "Failed to edit student.")
        return render(request,
                      'business/admin/actions/student_edit.html',
                      {'form': form, 'student': student, 'student_id': student_id})


class DeleteStudentView(View):
    def get(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, pk=student_id)
        return render(request,
                      'business/admin/actions/student_delete.html',
                      {'student': student, 'student_id': student_id})

    def post(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, pk=student_id)
        student.delete()
        messages.success(
            request, "Student Deleted Successfully.")
        return redirect('list_student')


class CreateProductView(View):
    """Creats a user product"""
    def get(self, request):
        form = AddProductForm()
        return render(request, 'business/admin/actions/products.html', {'form': form})

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        user_object = get_user_object(request.user)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save yet
            product.owner = request.user  # Set owner to current user
            product.save()
            messages.success(
                request, "Product Added Successfully.")
            if isinstance(user_object, BusinessUser):
                return redirect('business:log_products')
            elif isinstance(user_object, CreatorUser):
                return redirect('patron:history', kwags={'user':user_object})
        else:
            messages.error(
                request, "Failed to create product.")
        return render(request, 'business/admin/actions/products.html', {'form': form})


class EditProductView(View):
    """Edits a users product"""
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(
            Product, pk=product_id)  # Fetch product by ID
        # Pre-populate form with product data
        form = AddProductForm(instance=product)
        return render(request, 'business/admin/actions/product_edit.html', {'form': form, 'product': product, 'product_id': product_id})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        form = AddProductForm(request.POST, request.FILES, instance=product)
        user_object = get_user_object(request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Product Edited Successfully.")
            if isinstance(user_object, BusinessUser):
                return redirect('business:log_products')
            elif isinstance(user_object, CreatorUser):
                return redirect('patron:history', kwags={'user':user_object})
        else:
            messages.error(
                request, "Failed to edit product.")
        return render(request, 'business/admin/actions/product_edit.html', {'form': form, 'product': product, 'product_id': product_id})


class DeleteProductView(View):
    """Deletes a user products"""
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        return render(request,
                      'business/admin/actions/product_delete.html',
                      {'product': product, 'product_id': product_id})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        user_object = get_user_object(request.user)
        messages.success(
            request, "Product Deleted Successfully.")
        if isinstance(user_object, BusinessUser):
            return redirect('business:log_products')
        elif isinstance(user_object, CreatorUser):
            return redirect('patron:history', kwags={'user':user_object})


def bnpl(request):
    return render(request, 'business/admin/bnpl.html')


# Logs
@login_required
def log_transfer(request):
    return render(request, 'business/admin//log/transfer.html')


@login_required
def list_student(request):
    context = {}
    user_object = get_object_or_404(BusinessUser, username=request.user)
    students = Student.objects.filter(school=user_object.id)
    context['students'] = students
    return render(request, 'business/admin/log/student.html', context)


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
