from django import forms
from lipila.models import CustomerMessage
from django.contrib.auth.forms import UserChangeForm
from accounts.models import PatronProfile, CreatorProfile
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class ContactForm(forms.ModelForm):
    class Meta:
        model = CustomerMessage
        fields = ('name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Your WhatsApp number'}),
            'subject': forms.TextInput(attrs={'placeholder':'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'}),
        }


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=5, validators=[MinValueValidator(5, message='Minimum deposit amount is ZMW 5')])
    phone_number = forms.CharField(max_length=20)


class ContributeForm(forms.Form):
    amount = forms.DecimalField(min_value=50, validators=[MinValueValidator(5, message='Minimum deposit amount is ZMW 50')])
    phone_number = forms.CharField(max_length=20)