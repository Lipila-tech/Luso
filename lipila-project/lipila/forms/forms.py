from django import forms
from lipila.models import CustomerMessage
from patron.models import Contributions, ISP_CHOICES
from django.core.validators import MinValueValidator
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from patron.models import WithdrawalRequest, Tier, SubscriptionPayments, Transfer


class BaseTransactionForm(BSModalModelForm):
    wallet_type = forms.ChoiceField(choices=ISP_CHOICES)
    payer_account_number = forms.CharField(max_length=300)
    description = forms.CharField(max_length=200, required=False)

    class Meta:
        labels = {
            'payer_account_number': 'Account number'
        }


class TransferForm(BaseTransactionForm):
    send_money_to = forms.CharField(max_length=300)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['wallet_type', 'amount', 'payer_account_number', 'send_money_to',
                   'description']


class SubscriptionPaymentsForm(BaseTransactionForm):
    class Meta:
        model = SubscriptionPayments
        fields = ['wallet_type', 'payer_account_number',
                  'description']
        

class ContributionsForm(BaseTransactionForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Contributions
        fields = ['wallet_type', 'payer_account_number', 'amount',
                  'description']


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