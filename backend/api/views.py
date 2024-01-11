from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import (
    Payment, Student, LoanRequest,
    LoanPayment, School, Parent)

from .serializers import PaymentSerializer
from .serializers import LoanPaymentSerializer
from .serializers import StudentSerializer
from .serializers import LoanRequestSerializer
from .serializers import ParentSerializer
from .serializers import SchoolSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer


from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response


from django.shortcuts import render




def index(request):
    """View for the page homapage"""
    return render(request, 'index.html')
    
class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
  

class LoanRequestView(viewsets.ModelViewSet):
    serializer_class = LoanRequestSerializer
    queryset = LoanRequest.objects.all()

class LoanPaymentView(viewsets.ModelViewSet):
    serializer_class = LoanPaymentSerializer
    queryset = LoanPayment.objects.all()

class SchoolView(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()


class ParentView(viewsets.ModelViewSet):
    serializer_class = ParentSerializer
    queryset = Parent.objects.all()


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """POST request to get session Cookies:
            csrf and sessionid
        """
        serializer = LoginSerializer(
            data=self.request.data,
            context={ 'request': self.request }
            )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(str(user), status=status.HTTP_202_ACCEPTED)

class LogoutView(views.APIView):
    """" Logs out the current signed in user"""

    def get(self, request, format=None):
        """GET request to flash user cookies and log them out"""
        logout(request)
        return Response(status=status.HTTP_200_OK)

class ProfileView(viewsets.ModelViewSet):
    """Returns the profile of the user"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
