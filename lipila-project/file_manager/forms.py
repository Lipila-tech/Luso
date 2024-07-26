from django import forms
from .models import UploadedFile


class UploadFileForm(forms.Form):
    file = forms.FileField()


class EditMediaFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['short_description', 'long_description', 'is_private', 'tiers']

        labels = {
            'short_description': 'Title',
            'long_description': 'Description',
            'is_private':'Private'
        }