from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import CreatorProfile, PatronProfile


class CreateCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'account_number',
            'bio',
            'city',
            'creator_category',
            'facebook_url',
            'twitter_url',
            'instagram_url',
            'linkedin_url',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'rows': 5}),
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
