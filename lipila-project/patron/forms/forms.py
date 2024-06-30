from django.contrib.auth.models import User
from django import forms
from accounts.models import CreatorProfile, PatronProfile
from patron.models import Tier, WithdrawalRequest
from django.contrib.auth.forms import UserChangeForm


class DefaultUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        # Specify fields to exclude
        exclude = ('username', 'email', 'last_login', 'date_joined', 'groups',
                   'user_permissions', 'is_staff', 'password', 'is_superuser', 'is_active')


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['payment_method', 'amount', 'account_number']


class CreateCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'patron_title',
            'about',
            'creator_category',
            'city',
        ]


class EditCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'profile_image',
            'patron_title',
            'about',
            'creator_category',
            'city',
            'account_number',
            'facebook_url',
            'twitter_url',
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
