from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (BusinessUser, LipilaCollection, LipilaDisbursement)
from business.models import Product, BNPL, Invoice, InvoiceBusinessUser

class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = ('id', 'username', 'city', 'email', 'password',
                  'account_number', 'bio', 'business_category')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = BusinessUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LipilaCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = ('payer', 'payee', 'amount', 'description')