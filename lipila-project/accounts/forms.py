from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['password1'].help_text="Your password can't be too similar to your username."
      self.fields['password2'].help_text='Confirm password.'

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', )
        help_texts = {
            'username': None,
            'email': None,
        }
      
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user