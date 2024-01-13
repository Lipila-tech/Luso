from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import (
    Payment, Student, School, Parent, LipilaPayment)

from .serializers import SchoolPaymentSerializer
from .serializers import StudentSerializer
from .serializers import ParentSerializer
from .serializers import SchoolSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer
from .serializers import LipilaPaymentSerializer
from .serializers import LipilaTransactionSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render

from rest_framework.views import APIView
from api.momo.mtn import Collections
from api.helpers import unique_id

def index(request):
    """View for the page homapage"""
    return render(request, 'index.html')




class UserTransactionsView(viewsets.ModelViewSet):
    serializer_class = LipilaTransactionSerializer
    queryset = LipilaPayment.objects.all()

    def list(self, request):
        account = request.query_params.get('account')  # Get account from query parameters
        role = request.query_params.get('role')  # Get role (payer or receiver)

        if not account or not role:
            return Response({'error': 'Missing account or role parameter'}, status=400)

        if role == 'payer':
            transactions = LipilaPayment.objects.filter(payer_account=account)
        elif role == 'receiver':
            transactions = LipilaPayment.objects.filter(receiver_account=account)
        else:
            return Response({'error': 'Invalid role'}, status=400)

        serializer = LipilaTransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class PaymentView(viewsets.ModelViewSet):
    serializer_class = SchoolPaymentSerializer
    queryset = Payment.objects.all()


class LipilaCollectionView(viewsets.ModelViewSet):
    serializer_class = LipilaPaymentSerializer
    queryset = LipilaPayment.objects.all()

    

    def create(self, request):
        """Handles POST requests, deserializing date and setting status."""
        data = request.data
        serializer = LipilaPaymentSerializer(data=data)
        api_user = Collections()
        api_user.provision_sandbox(api_user.subscription_col_key)
        api_user.create_api_token(api_user.subscription_col_key, 'collection')
    
        if serializer.is_valid():
            try:
                # Query external API handlers
                amount = data['amount']
                reference_id = Collections().x_reference_id
                payer_account = data['payer_account']
                
                # Query request to pay function
                request_pay = api_user.request_to_pay(
                    amount=amount, payer_account=payer_account, reference=str(reference_id))
                
                if request_pay.status_code == 202:
                    # save payment
                    payment = serializer.save()
                    payment.reference_id = reference_id
                    payment.status = 'pending'  # Set status based on mapping
                    payment.save()

                    status_code = request_pay.status_code
                    return Response({'message': 'request accepted, wait for client approval'}, status=status_code)  # Set status code
                
                elif request_pay.status_code == 403:
                    status_code = request_pay.status_code 
                    return Response({'message': 'Request exceeded'}, status=status_code)  # Set status code
                
                elif request_pay.status_code == 400:
                    status_code = request_pay.status_code 
                    return Response({'message': 'Bad request'}, status=status_code)  # Set status code
                
            except Exception as e:
                print('Error:', e)
                return Response({'message': 'Error'}, status=400)  # Set status code
        else:
            return Response({'message': 'Invalid form fields'}, status=405)  # Set status code
            

    def list(self, request, *args, **kwargs):
        """Handles GET requests, serializing payment data."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
  

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
