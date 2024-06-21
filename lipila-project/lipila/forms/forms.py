from django import forms
from lipila.models import CustomerMessage
from patron.models import Contributions
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
    payer_account_number = forms.CharField(max_length=20)
    payment_method = forms.CharField(max_length=20)
    description = forms.CharField(max_length=20)


class ContributeForm(forms.ModelForm):
    class Meta:
        model = Contributions
        fields = ('amount', 'account_number', 'payment_method', 'description')