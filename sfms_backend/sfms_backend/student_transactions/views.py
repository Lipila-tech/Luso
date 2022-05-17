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

class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    

class TermView(viewsets.ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all()

class ProgramView(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()