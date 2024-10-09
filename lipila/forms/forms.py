from django import forms
from lipila.models import CustomerMessage
from patron.models import Payment
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from patron.models import WithdrawalRequest, Tier, SubscriptionPayments, Transfer
from django.contrib.auth import get_user_model
from accounts.models import CreatorProfile
from django.shortcuts import get_object_or_404
from accounts.globals import ISP_CHOICES


# Define the form
class MoneyTransferForm(forms.Form):
    WALLET_CHOICES = [
        ('mtn', 'MTN Mobile Money'),
        ('airtel', 'Airtel Money'),
    ]
    
    wallet_type = forms.ChoiceField(choices=WALLET_CHOICES, label="Wallet Type")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
    recipient_phone_number = forms.CharField(max_length=15, label="Recipient Phone Number")
    sender_phone_number = forms.CharField(max_length=15, label="Sender Phone Number")
    transaction_reference = forms.CharField(max_length=50, required=False, label="Transaction Reference (Optional)")
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("The amount must be greater than zero.")
        return amount


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
       

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['wallet_type', 'msisdn', 'amount',
                  'reference', 'payee']
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
