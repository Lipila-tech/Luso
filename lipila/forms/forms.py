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
    msisdn = forms.CharField(max_length=300)
    reference = forms.CharField(max_length=200, required=False)

    class Meta:
        labels = {
            'msisdn': 'Account number'
        }


class TransferForm(BaseTransactionForm):
    send_money_to = forms.CharField(max_length=300)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['wallet_type', 'amount', 'msisdn', 'send_money_to',
                  'reference']


class SubscriptionPaymentsForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPayments
        fields = ['amount', 'msisdn',
                  'reference', "wallet_type", 'payee']

        labels = {'msisdn': 'Mobile number'}

        widgets = {
            'msisdn': forms.TextInput(attrs={'placeholder': 'Ex. 076433223'}),
            'reference': forms.TextInput(attrs={'placeholder': 'Ex. Firstname lastname'}),
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
        fields = ['wallet_type', 'msisdn', 'amount',
                  'reference', 'payee', 'payer']
        labels = {'msisdn': 'Pay using:', "reference": 'Message'}

        widgets = {
            'msisdn': forms.TextInput(attrs={'placeholder': 'Ex. 076433223'}),
            'reference': forms.TextInput(attrs={'placeholder': 'Ex. I would love to chat with you.'}),
        }

    def __init__(self, *args, **kwargs):
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
        

class UnUthSupportPaymentForm(forms.ModelForm):
    class Meta:
        model = ContributionsUnauth
        fields = ['wallet_type', 'msisdn', 'amount',
                  'reference', 'payee', 'payer']
        labels = {'msisdn': 'Pay using:', "reference": 'Message', 'payer': 'Email or Phone:'}

        widgets = {
            'msisdn': forms.TextInput(attrs={'placeholder': 'Ex. 076433223'}),
            'reference': forms.TextInput(attrs={'placeholder': 'Ex. I would love to chat with you.'}),
        }

    def __init__(self, *args, **kwargs):
        payee = kwargs.pop('payee')
        super().__init__(*args, **kwargs)
        self.fields['wallet_type'].widget.attrs['hidden'] = True
        self.fields['payee'].widget.attrs['hidden'] = True
        self.fields['payee'].initial = get_object_or_404(
            CreatorProfile, patron_title=payee)
       

class WithdrawalModelForm(BSModalModelForm):
    class Meta:
        model = WithdrawalRequest
        exclude = ['creator', 'transaction_id',
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
