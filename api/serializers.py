from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (LipilaCollection, LipilaDisbursement)
from patron.models import SubscriptionPayments
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL
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


class LipilaCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = ['payer_account_number', 'amount',
                  'wallet_type', 'description']


class LipilaDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaDisbursement
        fields = ['send_money_to', 'amount',
                  'wallet_type', 'description']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        mdodel = SubscriptionPayments
        fields = ['amount', 'payer_account-number', 'description', 'wallet_type']
