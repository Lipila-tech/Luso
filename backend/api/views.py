from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import (
    Payment, Student, School, Parent, LipilaPayment)

from .serializers import PaymentSerializer
from .serializers import StudentSerializer
from .serializers import ParentSerializer
from .serializers import SchoolSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer
from .serializers import LipilaPaymentSerializer

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render

from api.external_api_handler import MtnApiHandler

def index(request):
    """View for the page homapage"""
    return render(request, 'index.html')
    
class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

class LipilaPaymentView(viewsets.ModelViewSet):
    serializer_class = LipilaPaymentSerializer
    queryset = LipilaPayment.objects.all()

    def create(self, request):
        """Handles POST requests, deserializing date and setting status."""
        data = request.data
        serializer = LipilaPaymentSerializer(data=data)

        if serializer.is_valid():
            try:
                # Query external API handlers
                api_user = MtnApiHandler()
                api_user.create_api_user()
                api_user.get_api_key()
                api_user.get_api_token()

                amount = data['amount']
                reference_id = 0 + 100
                description = data['description']
                payer_account = data['payer_account']
                payer_name = data['payer_name']
                payer_email = data['payer_email']
                receiver_account = data['receiver_account']
                status = 'pending'
                
                # Query request to pay function
                request_pay = api_user.request_to_pay(
                    amount=amount, payer_account=payer_account, reference=str(reference_id))
                
                if request_pay.status_code == 202:
                    # save payment
                    payment = serializer.save()
                    payment.status = 'success'  # Set status based on mapping
                    # payment.timestamp = payment.timestamp.replace(tzinfo=None)  # Remove timezone
                    payment.save()

                    # code to auto deduct commision before saving to subscriber data.
                    #donation_amount = int(donation_amount) * (95/100)

                    status_code = request_pay.status_code
                    return Response({'message': 'Payment processed'}, status=status_code)  # Set status code
                
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
            return Response({'message': 'Invalid form fields'}, status=400)  # Set status code
            

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
