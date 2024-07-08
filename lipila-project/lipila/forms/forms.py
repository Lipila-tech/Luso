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
        fields = ['network_operator', 'account_number', 'amount']


class TierModelForm(BSModalModelForm):
    class Meta:
        model = Tier
        exclude = ['updated_at']
                

class SendMoneyForm(BSModalModelForm):
    class Meta:
        model = Contributions
        fields = ('amount', 'payer_account_number', 'network_operator', 'description')

        
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