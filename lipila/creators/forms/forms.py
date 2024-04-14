from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from creators.models import CreatorUser

class LoginForm(forms.ModelForm):
    class Meta:
        model = CreatorUser
        fields = ('username', 'password')


class SignupForm(forms.ModelForm):
    class Meta:
        model = CreatorUser
        fields = ('creator_category', 'username', 'email', 'password')


class EditCreatorUserForm(UserChangeForm):
    class Meta:
        model = CreatorUser
        fields = [
            'profile_image',
            'first_name',
            'last_name',
            'phone_number',
            'bio',
            'city',
            'address',
            'company',
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