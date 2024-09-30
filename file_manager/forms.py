from django import forms
from .models import UploadedFile
from patron.models import Tier

class UploadFileForm(forms.Form):
    file = forms.FileField()


class EditMediaFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['short_reference',
                  'long_reference', 'is_private', 'tiers']

        labels = {
            'short_reference': 'Title',
            'long_reference': 'reference',
            'is_private': 'Private',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['tiers'].queryset = Tier.objects.filter(creator=user)
