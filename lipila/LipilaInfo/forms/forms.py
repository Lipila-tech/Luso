from django import forms
from LipilaInfo.models import CustomerMessage
from django.contrib.auth.forms import UserChangeForm
from patron.models import Patron, CreatorUser
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


class EditUserForm(UserChangeForm):
    class Meta:
        model = CreatorUser
        fields = [
            'profile_image',
            'account_number',
            'city',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


# class JoinForm(forms.ModelForm):
#     class Meta:
#         model = Patron
#         fields = ('subscription',)
       