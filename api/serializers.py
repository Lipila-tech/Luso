from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import MomoColTransaction, LipilaDisbursement, MomoColTransaction
from patron.models import SubscriptionPayments
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL


class MomoColTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomoColTransaction
        fields = ['reference', 'transaction_id', 'msisdn', 'amount',
                  'status', 'wallet_type', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LipilaDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaDisbursement
        fields = ['send_money_to', 'amount',
                  'wallet_type', 'transaction_id']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        mdodel = SubscriptionPayments
        fields = ['amount', 'payer_account-number',
                  'transaction_id', 'wallet_type']
