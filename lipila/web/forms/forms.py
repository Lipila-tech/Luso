from django.contrib.auth.models import User
from django import forms
from api.models import LipilaDisbursement
from web.models import LipilaUser

class DisburseForm(forms.ModelForm):
    class Meta:
        model = LipilaDisbursement
        fields = '__all__'


class LoginForm(forms.ModelForm):
    class Meta:
        model = LipilaUser
        fields = ('username', 'password')


class SignupForm(forms.ModelForm):
    class Meta:
        model = LipilaUser
        fields = ('username', 'city', 'user_category', 'phone_number', 'password')


class EditLipilaUserForm(forms.ModelForm):
    class Meta:
        model = LipilaUser
        fields = ['profile_image', 'phone_number', 'bio', 'country', 'city', 'address', 'company', 'user_category']
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),  # Restrict file types
        }

    def __init__(self, *args, **kwargs):
        super(EditLipilaUserForm, self).__init__(*args, **kwargs)
        # Exclude email field as it's likely not editable by the user
        self.fields['country'].disabled = True