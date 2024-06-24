from django import forms
from accounts.models import CreatorProfile, PatronProfile
from patron.models import Tier, WithdrawalRequest


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'account_number']

class CreateCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
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
