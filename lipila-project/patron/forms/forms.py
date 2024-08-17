from django.contrib.auth import get_user_model
from django import forms
from accounts.models import CreatorProfile, PayoutAccount
from patron.models import Tier, WithdrawalRequest
from django.contrib.auth.forms import UserChangeForm


class DefaultUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        # Specify fields to exclude
        exclude = ('username', 'email', 'last_login', 'date_joined', 'groups',
                   'user_permissions', 'is_staff', 'password', 'is_superuser',
                   'is_active', 'has_group', 'is_creator')


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['wallet_type', 'amount', 'account_number']


class CreateCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'adults_group',
            'creator_category',
            'patron_title',
            'location',
            'country',
        ]

        labels = {
            'adults_group': 'My page is not suitable for people under 18.',
            'patron_title': 'Name your Page',
            'creator_category': 'Choose your category',
            'location': 'Choose your location',
        }

        widgets = {
            'patron_title': forms.TextInput(attrs={'placeholder': 'Your creator name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs['readonly'] = True


class EditCreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'profile_image',
            'patron_title',
            'about',
            'creator_category',
            'creator_id_file',
            'location',
            'facebook_url',
            'twitter_url',
        ]

        labels = {
            'creator_id_file': 'Upload ID*'
        }
        widgets = {
            # Restrict file types
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class PayoutAccountEditFrom(forms.ModelForm):
    class Meta:
        model = PayoutAccount
        fields = ['wallet_type', 'wallet_provider', 'account_name', 'account_number']



class EditTiersForm(forms.ModelForm):
    class Meta:
        model = Tier
        fields = [
            'name',
            'description',
            'price',
            'visible_to_fans',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
