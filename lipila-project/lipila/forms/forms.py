from django import forms
from lipila.models import CustomerMessage
from patron.models import Contributions, ISP_CHOICES
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from patron.models import WithdrawalRequest, Tier

class WithdrawalModelForm(BSModalModelForm):
    class Meta:
        model = WithdrawalRequest
        exclude = ['creator', 'reference_id', 'processed_date', 'request_date', 'status']
        labels = {
            'reason': 'Reference'
        }
       

class TierModelForm(BSModalModelForm):
    class Meta:
        model = Tier
        exclude = ['updated_at']
                

class SendMoneyForm(BSModalForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    network_operator = forms.CharField(max_length=50)
    payer_account_number = forms.CharField(max_length=20)
    description = forms.CharField(max_length=255, required=False)
    payee_account_number = forms.CharField(max_length=20, required=False)

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = self.initial.get('transaction_type')

        if transaction_type == 'transfer' and not cleaned_data.get('payee_account_number'):
            self.add_error('payee_account_number', 'This field is required for transfers.')

        return cleaned_data

        
class ContactForm(forms.ModelForm):
    class Meta:
        model = CustomerMessage
        fields = ('name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Your WhatsApp number'}),
            'subject': forms.TextInput(attrs={'placeholder':'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'}),
        }


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=5, validators=[MinValueValidator(10, message='Minimum deposit amount is ZMW 5')], required=True)
    payer_account_number = forms.CharField(max_length=20, required=True)
    network_operator = forms.ChoiceField(choices=ISP_CHOICES)
    description = forms.CharField(max_length=300, required=False)
    

class ContributeForm(forms.ModelForm):
    class Meta:
        model = Contributions
        fields = ('amount', 'payer_account_number', 'network_operator', 'description')