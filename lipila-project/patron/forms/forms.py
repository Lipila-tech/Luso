from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import CreatorProfile, PatronProfile


class EditCreatorProfileForm(UserChangeForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'profile_image',
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
        }


class EditPatronProfileForm(UserChangeForm):
    class Meta:
        model = PatronProfile
        fields = [
            'profile_image',
            'account_number',
            'city',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
