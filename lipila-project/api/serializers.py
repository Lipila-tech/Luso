from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (LipilaCollection, LipilaDisbursement)
from patron.models import SubscriptionPayments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
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
        fields = ['payee_account_number', 'amount',
                  'wallet_type', 'description']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        mdodel = SubscriptionPayments
        fields = ['amount', 'payer_account-number', 'description', 'wallet_type']
