from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import CreatorProfile, PatronProfile
from patron.models import Tier
from django.core.validators import MinValueValidator


class CreateCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'patron_title',
            'bio',
            'creator_category',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class CreatePatronProfileForm(forms.ModelForm):
    class Meta:
        model = PatronProfile
        fields = [
            'account_number',
            'city',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class EditTiersForm(forms.ModelForm):
    class Meta:
        model = Tier
        fields = [
            'name',
            'description',
            'price',
            'visible_to_fans',
        ]

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=5, validators=[MinValueValidator(5, message='Minimum deposit amount is ZMW 5')])
    phone_number = forms.CharField(max_length=20)

class ContributeForm(forms.Form):
    amount = forms.DecimalField(min_value=50, validators=[MinValueValidator(5, message='Minimum deposit amount is ZMW 50')])
    phone_number = forms.CharField(max_length=20)