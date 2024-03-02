from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import LipilaCollection, Product, MyUser, BNPL


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','username', 'city', 'email', 'password', 'phone_number', 'bio', 'business_type')
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
                  'description', 'payer_email', 'payer_name')


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
                  'description', 'payer_email',  'payer_name'
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
        # fields = [
        #     'requested_by',
        #     'product',
        #     'amount'
        # ]
        fields = '__all__'