from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from patron.models import CreatorUser, PatronUser

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = CreatorUser
#         fields = ('username', 'password')


class SignupForm(forms.ModelForm):
    class Meta:
        model = CreatorUser
        # fields = ('creator_category', 'username', 'email', 'password')
        fields = ('creator_category',)


class EditCreatorUserForm(UserChangeForm):
    class Meta:
        model = CreatorUser
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


class EditPatronUserForm(UserChangeForm):
    class Meta:
        model = PatronUser
        fields = [
            'profile_image',
            'account_number',
            'city',
            ]
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
