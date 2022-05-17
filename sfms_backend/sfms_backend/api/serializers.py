
from rest_framework import serializers
from .models import Payment, Student, Program, Term


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('student', 'term', 'amount', 'pay_date')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
  
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'