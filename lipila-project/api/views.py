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
from .serializers import UserSerializer
from .models import (LipilaCollection)
from api.momo.mtn import Collections


# Define global variables
env = environ.Env()
environ.Env.read_env()
User = get_user_model()


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
            payer = str(data['payer'])
            payee = str(data['payee'])
            amount = str(data['amount'])
            serializer = LipilaCollectionSerializer(data=data)
            api_user = Collections()
            api_user.provision_sandbox(api_user.subscription_col_key)
            api_user.create_api_token(
                api_user.subscription_col_key, 'collection')
            
            if serializer.is_valid():
                reference_id = api_user.x_reference_id
                request_pay = api_user.request_to_pay(
                    amount=amount, payer=payer, reference_id=str(reference_id))
                if request_pay.status_code == 202:
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
                            payment.reference_id = reference_id
                            payment.status = 'accepted'
                            payment.save()
                        else:
                            payment.status = 'failed'
                    payment.save()
                elif request_pay.status_code == 403:
                    status_code = request_pay.status_code
                    # Set status code
                    return Response({'message': 'Request exceeded'}, status=status_code)

                elif request_pay.status_code == 400:
                    status_code = request_pay.status_code
                    # Set status code
                    return Response({'message': 'Bad request from mtn'}, status=status_code)

        except Exception as e:
            
            return Response({'message': f'Key Error in submitted data {e}'}, status=400)
        return Response({'message': 'request accepted, wait for client approval'}, status=202)
        

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