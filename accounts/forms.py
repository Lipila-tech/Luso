from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Use PasswordInput widget

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user