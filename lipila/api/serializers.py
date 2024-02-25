from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import LipilaPayment, Product, MyUser, BusinessPayment


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'phone_number', 'bio')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LipilaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaPayment
        fields = ('payee', 'payer_account', 'amount', 'timestamp',
                  'description', 'payer_email', 'payer_name')


class BusinessPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPayment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LipilaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaPayment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'bio',
            'phone_number'
        ]
