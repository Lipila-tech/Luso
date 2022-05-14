from rest_framework import viewsets
from .serializers import PaymentSerializer
from .serializers import TermSerializer
from .serializers import StudentSerializer
from .serializers import ProgramSerializer
from .models import Payment, Student, Term, Program

# Create your views here.
class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def payment(id):
        """ Returns a students payment records"""
        student = Student.objects.get(pk=id)
        payments = student.payment.all()
        return payments


class StudentView(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class TermView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all()

class ProgramView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
