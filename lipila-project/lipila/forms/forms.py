from django import forms
from lipila.models import CustomerMessage
from patron.models import Contributions, ContributionsUnauth
from django.core.validators import MinValueValidator
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from patron.models import WithdrawalRequest, Tier, SubscriptionPayments, Transfer
from django.contrib.auth import get_user_model
from accounts.models import CreatorProfile
from django.shortcuts import get_object_or_404
from accounts.globals import ISP_CHOICES



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


class SubscriptionPaymentsForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPayments
        fields = ['amount', 'payer_account_number',
                  'description', "wallet_type", 'payee']

        labels = {'payer_account_number': 'Mobile number'}

        widgets = {
            'payer_account_number': forms.TextInput(attrs={'placeholder': 'Ex. 076433223'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ex. Firstname lastname'}),
        }

    def __init__(self, *args, **kwargs):
        amount = kwargs.pop('amount', None)
        payee = kwargs.pop('payee')
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['hidden'] = True
        self.fields['wallet_type'].widget.attrs['hidden'] = True
        self.fields['payee'].widget.attrs['hidden'] = True
        # Set the initial value for the amount field
        if amount is not None:
            self.fields['amount'].initial = amount
        self.fields['payee'].initial = payee


class SupportPaymentForm(forms.ModelForm):
    class Meta:
        model = Contributions
        fields = ['wallet_type', 'payer_account_number', 'amount',
                  'description', 'payee', 'payer']
        labels = {'payer_account_number': 'Pay using:', "description": 'Message'}

        widgets = {
            'payer_account_number': forms.TextInput(attrs={'placeholder': 'Ex. 076433223'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ex. I would love to chat with you.'}),
        }

    def __init__(self, *args, **kwargs):
        amount = kwargs.pop('amount', None)
        payee = kwargs.pop('payee')
        payer = kwargs.pop('payer')
        super().__init__(*args, **kwargs)
        self.fields['wallet_type'].widget.attrs['hidden'] = True
        self.fields['payee'].widget.attrs['hidden'] = True
        self.fields['payer'].widget.attrs['hidden'] = True
        self.fields['payee'].initial = get_object_or_404(
            CreatorProfile, patron_title=payee)
        self.fields['payer'].initial = get_user_model(
        ).objects.get(username=payer)
        if amount is not None:
            self.fields['amount'].initial = amount


class UnUthSupportPaymentForm(forms.ModelForm):
    class Meta:
        model = ContributionsUnauth
        fields = ['wallet_type', 'payer_account_number', 'amount',
                  'description', 'payee', 'payer']
        labels = {'payer_account_number': 'Pay using:', "description": 'Message'}

        widgets = {
            'payer_account_number': forms.TextInput(attrs={'placeholder': 'Ex. 076433223'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ex. I would love to chat with you.'}),
        }

    def __init__(self, *args, **kwargs):
        amount = kwargs.pop('amount', None)
        payee = kwargs.pop('payee')
        super().__init__(*args, **kwargs)
        self.fields['wallet_type'].widget.attrs['hidden'] = True
        self.fields['payee'].widget.attrs['hidden'] = True
        self.fields['payer'].widget.attrs['hidden'] = True
        self.fields['payee'].initial = get_object_or_404(
            CreatorProfile, patron_title=payee)
        if amount is not None:
            self.fields['amount'].initial = amount


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
        exclude = ['updated_at', 'creator', 'is_editable']


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
