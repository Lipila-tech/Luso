from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import (
    Payment, Student,
    School, Parent)
from rest_framework import serializers
from .models import LipilaPayment, Product, MyUser
# from rest_framework.authtoken.serializers import ObtainAuthTokenSerializer


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
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LipilaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaPayment
        fields = '__all__'

class SchoolPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
    
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

# class MyLoginSerializer(ObtainAuthTokenSerializer):
#     username_field = MyUser.USERNAME_FIELD  # Use your custom field

#     def validate(self, attrs):
#         # Add custom validations like checking phone number, active status, etc.
#         return super().validate(attrs)


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
