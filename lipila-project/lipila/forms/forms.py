from django import forms
from lipila.models import CustomerMessage
from django.contrib.auth.forms import UserChangeForm
from accounts.models import PatronProfile, CreatorProfile
from django.contrib.auth.models import User


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
