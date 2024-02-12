from django import forms
from api.models import LipilaDisbursement

class DisburseForm(forms.ModelForm):
    class Meta:
        model = LipilaDisbursement
        fields = '__all__'
