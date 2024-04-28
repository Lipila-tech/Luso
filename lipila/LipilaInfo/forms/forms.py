from django import forms
from LipilaInfo.models import LipilaUserEmail, LipilaUser
from django.contrib.auth.forms import UserChangeForm
from creators.models import Patron


class ContactForm(forms.ModelForm):
    class Meta:
        model = LipilaUserEmail
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
        model = LipilaUser
        fields = ('username', 'email', 'password')


class EditLipilaUserForm(UserChangeForm):
    class Meta:
        model = LipilaUser
        fields = [
            'profile_image',
            'first_name',
            'last_name',
            'phone_number',
            'city',
            'address',
            'company',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


# class JoinForm(forms.ModelForm):
#     class Meta:
#         model = Patron
#         fields = ('subscription',)
       