import environ
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# My modules
from .serializers import LipilaCollectionSerializer
from .serializers import BusinessUserSerializer
from .models import (BusinessUser, LipilaCollection)
from business.models import (Product, BNPL, Invoice, InvoiceBusinessUser)
from api.momo.mtn import Collections


# Define global variables
env = environ.Env()
environ.Env.read_env()
User = get_user_model()


class SignupViewSet(viewsets.ModelViewSet):
    """Register API user"""
    queryset = BusinessUser.objects.all()
    serializer_class = BusinessUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': "Created",
            }, status=201)
        except Exception as e:
            return Response({"Error": e}, status=400)

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            # Set password, send verification email, etc. (optional)
        except Exception as e:
            return Response({"Error": e}, status=400)

    permission_classes = [AllowAny]  # Allow anyone to register


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'username': user.username,
                    'user_id': user.pk
                }
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({"Error: Bad Request"}, status=400)


class LipilaCollectionView(viewsets.ModelViewSet):
    """Collects Payments for registered users."""
    serializer_class = LipilaCollectionSerializer
    queryset = LipilaCollection.objects.all()
    
    def create(self, request):
        """Handles POST requests, deserializing date and setting status."""
        try:
            data = request.data
            payer = data['payer']  # Access the first value for 'payer'
            payee = data['payee'] # Access the first value for 'payee'
            amount = data['amount'] # Access the first value for 'amount'
            description = data['description']  # Access the first value for 'description'

            serializer = LipilaCollectionSerializer(data=data)
            print(serializer)
        
            api_user = Collections()
            api_user.provision_sandbox(api_user.subscription_col_key)
            api_user.create_api_token(
                api_user.subscription_col_key, 'collection')

            if serializer.is_valid():
                print('VALID SER')
            # try:
                # Query external API handlers
                amount = data['amount']
                reference_id = api_user.x_reference_id
                payer_account = '8877665544'

                # Query request to pay function
                request_pay = api_user.request_to_pay(
                    amount=amount, payer_account=payer_account, reference=str(reference_id))

                if request_pay.status_code == 202:
                    print('PAYMENT SENT SUCCESS')
                    # save payment
                    payment = serializer.save()
                    payment.reference_id = reference_id
                    payment.status = 'pending'  # Set status based on mapping
                    payment.save()
                    transaction = LipilaCollection.objects.filter(
                        reference_id=reference_id)
                    for r in transaction:
                        status = api_user.get_payment_status(reference_id)
                        if status.status_code == 200:
                            payment.status = 'success'
                            payment.save()
                        else:
                            payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    # Set status code
                    return Response({'message': 'request accepted, wait for client approval'}, status=status_code)

                elif request_pay.status_code == 403:
                    status_code = request_pay.status_code
                    # Set status code
                    return Response({'message': 'Request exceeded'}, status=status_code)

                elif request_pay.status_code == 400:
                    status_code = request_pay.status_code
                    # Set status code
                    return Response({'message': 'Bad request from mtn'}, status=status_code)

        except Exception as e:
            return Response({'message': e}, status=400)
        else:
            # Set status code
            return Response({'message': 'Invalid form fields'}, status=405)

    def list(self, request):
        try:
            payee = request.query_params.get('payee')

            if not payee:
                return Response({"error": "payee id is missing"}, status=400)
            else:
                user = User.objects.get(username=payee)
                payments = LipilaCollection.objects.filter(payee=user.id)

            serializer = LipilaCollectionSerializer(payments, many=True)
            return Response(serializer.data, status=200)

        except User.DoesNotExist:
            return Response({"error": "Payee not found"}, status=404)


class LogoutView(views.APIView):
    """" Logs out the current signed in user"""

    def get(self, request, format=None):
        """GET request to flash user cookies and log them out"""
        logout(request)
        return Response(status=status.HTTP_200_OK)