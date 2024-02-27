from django.contrib.auth.models import User
from django import forms
from api.models import LipilaDisbursement, MyUser

class DisburseForm(forms.ModelForm):
    class Meta:
        model = LipilaDisbursement
        fields = '__all__'


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        

class SignupForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'phone_number', 'password')