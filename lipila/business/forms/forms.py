from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from api.models import LipilaDisbursement
from business.models import BusinessUser, Product, Student


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'other_name', 'tuition', 'address', 'grade', 'active')

class DisburseForm(forms.ModelForm):
    class Meta:
        model = LipilaDisbursement
        fields = '__all__'


class LoginForm(forms.ModelForm):
    class Meta:
        model = BusinessUser
        fields = ('username', 'password')


class SignupForm(forms.ModelForm):
    class Meta:
        model = BusinessUser
        fields = ('business_category', 'username', 'email', 'password')


class EditBusinessUserForm(UserChangeForm):
    class Meta:
        model = BusinessUser
        fields = [
            'profile_image',
            'first_name',
            'last_name',
            'account_number',
            'bio',
            'city',
            'address',
            'company',
            'business_category',
            'facebook_url',
            'twitter_url',
            'instagram_url',
            'linkedin_url',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity',)