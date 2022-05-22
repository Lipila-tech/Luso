from django.contrib.auth import login, logout

from .models import Payment, Program, Student, Term

from .serializers import PaymentSerializer
from .serializers import TermSerializer
from .serializers import StudentSerializer
from .serializers import ProgramSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import api_view

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import TokenAuthentication

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import render

#from .external_api_handler import Handler


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        """ List all payments"""
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Create a new payment"""
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
  

class TermView(viewsets.ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all()

class ProgramView(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()


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
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(views.APIView):
    """" Logs out the currecnt signed in user"""

    def get(self, request, format=None):
        """GET request to flash user cookies and log them out"""
        logout(request)
        return Response(status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    """Returns the profile of the user"""
    serializer_class = UserSerializer

    def get_object(self):
        """ GET the user object"""
        return self.request.user




