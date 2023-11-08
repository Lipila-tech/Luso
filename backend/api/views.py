from django.contrib.auth import login, logout
from django.core import serializers

from .models import Payment, Program, Student, Term

from .serializers import PaymentSerializer
from .serializers import HistorySerializer
from .serializers import StudentSerializer
from .serializers import ProgramSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer

from django.contrib.auth.models import User

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


# Create your views here.

def index(request):
    """View for the page homapage"""
    return render(request, 'index.html')
    
#@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        """ List all payments"""
        

        #payments = Payment.objects.all()
        #serializer = PaymentSerializer(payments, many=True)
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """Create a new payment"""
        from .external_api_handler import APIHandler

        # Get IDS and Validata request data
        student_pk = self.request.GET.get('id', '')
        if not User.objects.filter(pk=student_pk).values():
            return Response(
                {'Message': 'User not available'},
                status=status.HTTP_404_NOT_FOUND)

        if len(request.data) < 6:
            return Response(
                {'Message': 'Missing values'},
                status=status.HTTP_400_BAD_REQUEST)

        term_id = self.request.data['term']
        partyId = str(self.request.data['mobile'])
        externalId = str(self.request.data['reference'])
        amount = str(self.request.data['amount'])
             
        if len(partyId) != 10 or int(amount) < 100:
            return Response(
                {'Message': 'Invalid mobile and amount data'},
                status=status.HTTP_400_BAD_REQUEST)

        # Query external API handlers
        pay = APIHandler()
        pay.get_uuid()
        pay.create_api_user()
        pay.get_api_key()
        pay.get_api_token()

        try:
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                # Query request to pay function
                payer = pay.request_to_pay(amount, partyId,
                externalId)
                if payer.status_code == 202:
                    serializer.save()
                    # set variables
                    student = str(User.objects.get(pk=student_pk))
                    term = Term.objects.filter(pk=term_id).values()
                    term = term[0]['name']
                                               
                    content = {'student': student,
                    'amount': amount,
                    'account':partyId,
                    'reference':externalId,
                    'term': term
                    }
                    
                    return Response(content,
                        status=status.HTTP_201_CREATED)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                elif payer.status_code == 400:
                    raise ValueError('BAD REQUEST TO API')
                elif payer.status_code == 409:
                    raise TypeError('RESOURCE ALREADY EXITS')
                elif payer.status_code == 500:
                    raise TypeError('INTERNAL SERVER ERROR')
                elif payer.status_code == 403:
                    raise TypeError('EXCEEDED')
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        error = pay.request_to_pay(amount, partyId,
                externalId)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
  

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
        return Response(str(user), status=status.HTTP_202_ACCEPTED)

class LogoutView(views.APIView):
    """" Logs out the current signed in user"""

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


class HistoryView(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        """ List all payments"""
        payments = Payment.objects.all()
        serializer = HistorySerializer(payments, many=True)

        # Get IDS
        student_pk = request.GET.get('id', '')
        
        if not Student.objects.filter(username_id=student_pk).values():
            return Response(
                {'Message': 'User not a student'},
                status=status.HTTP_404_NOT_FOUND)

        # Get Values
        username = User.objects.filter(pk=student_pk).values()
        username = username[0]['username']
        content = Payment.objects.filter(student_id=student_pk).values()

        tuition = Student.objects.filter(username_id=student_pk).values()
        tuition = tuition[0]['tuition']

        if len(content) < 1:
            return Response(
                {'Message': 'No payment data available'},
                status=status.HTTP_204_NO_CONTENT)

        # Get data from json object to dict
        data = {}
        for json_data in content:
            for k, v in json_data.items():
                data[k] = v
        # Check if user has content
        term_pk = int(data['term_id'])
 
        term = Term.objects.filter(pk=term_pk).values()
        term = term[0]['name']

        balance = int(tuition) - int(data['amount'])

        context = {
            'student': username,
            'reference':data['reference'],
            'amount':data['amount'],
            'paydate':data['pay_date'],
            'account':data['mobile'],
            'term':term,
            'tuition':tuition,
            'pending': balance
            }

        return Response(context, status=status.HTTP_200_OK)