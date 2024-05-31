from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import CreatorProfile, PatronProfile
from patron.models import Tier

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
        ]