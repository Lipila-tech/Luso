from django.contrib.auth.models import User
from django import forms
from api.models import LipilaDisbursement, LipilaUser

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