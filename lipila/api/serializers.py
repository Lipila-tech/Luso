from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (LipilaCollection, Product, MyUser,
                     BNPL, Invoice, InvoiceLipilaUser, LipilaUserCollection)


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'city', 'email', 'password',
                  'phone_number', 'bio', 'business_type')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LipilaCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = ('payee', 'payer_account', 'amount', 'timestamp',
                  'description', 'payee')


class LipilaUserCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaUserCollection
        fields = ('payee', 'payer', 'amount', 'timestamp',
                  'description')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_owner', 'price',
                  'status'
                  ]


class LipilaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = ['payee', 'payer_account', 'amount'
                  'description', 'payer',  'payee'
                  ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'first_name',
            'last_name',
            'bio',
            'phone_number',
            'address',
            'city',
            'profile_image'
        ]
        write_only_fields = ('password', 'username')


class BNPLSerializer(serializers.ModelSerializer):
    class Meta:
        model = BNPL
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            'creator',
            'customer_name',
            'customer_phone_number',
            'customer_email',
            'due_date',
            'description',
            'total_amount',
            'status',
        )


class InvoiceLipilaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLipilaUser
        fields = (
            'creator',
            'receiver',
            'due_date',
            'description',
            'total_amount',
            'status',
        )
