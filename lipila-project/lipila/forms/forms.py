from django import forms
from lipila.models import CustomerMessage
from patron.models import Contributions, ISP_CHOICES
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from patron.models import WithdrawalRequest, Tier, SubscriptionPayments, Transfer


class BaseTransactionForm(BSModalModelForm):
    wallet_type = forms.ChoiceField(choices=ISP_CHOICES)
    payer_account_number = forms.CharField(max_length=300)
    description = forms.CharField(max_length=200, required=False)


class TransferForm(BaseTransactionForm):
    payee_account_number = forms.CharField(max_length=300)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['amount', 'payer_account_number', 'payee_account_number',
                  'wallet_type', 'description']


class SubscriptionPaymentsForm(BaseTransactionForm):
    class Meta:
        model = SubscriptionPayments
        fields = ['payer_account_number',
                  'wallet_type', 'description']
        labels = {
            'wallet_type': 'Wallet type'
        }


class ContributionsForm(BaseTransactionForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Contributions
        fields = ['amount', 'payer_account_number',
                  'wallet_type', 'description']


class WithdrawalModelForm(BSModalModelForm):
    class Meta:
        model = WithdrawalRequest
        exclude = ['creator', 'reference_id',
                   'processed_date', 'request_date', 'status']
        labels = {
            'reason': 'Reference'
        }


class TierModelForm(BSModalModelForm):
    class Meta:
        model = Tier
        exclude = ['updated_at', 'creator']


class ContactForm(forms.ModelForm):
    class Meta:
        model = CustomerMessage
        fields = ('name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Your WhatsApp number'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'}),
        }


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
