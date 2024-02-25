from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import LipilaCollection, Product, MyUser


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


class LipilaCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = ('payee', 'payer_account', 'amount', 'timestamp',
                  'description', 'payer_email', 'payer_name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LipilaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'bio',
            'phone_number',
            'country',
            'address',
            'city',
            'profile_image'
        ]
