import environ
from django.contrib.auth import login, logout
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.http import FileResponse, Http404
import os

from django.shortcuts import render, redirect

# My modules
from .serializers import LipilaCollectionSerializer, LipilaDisbursementSerializer, AirtelTransactionSerializer
from .models import LipilaCollection, LipilaDisbursement, AirtelTransaction
from api.momo.mtn import Collections, Disbursement
from .utils import get_api_user, generate_transaction_id
from .momo.openapi_client import ApiClient
from .momo.openapi_client.api.submit_payment_or_refund_request_api import SubmitPaymentOrRefundRequestApi
from .momo.airtel import AirtelMomo 

# Define global variables
User = get_user_model()


# Initialize the MTN API client
api_client = ApiClient()
api_instance = SubmitPaymentOrRefundRequestApi(api_client)

# Now `api_instance` can be used to make API calls
# response = api_instance.create_payment()

# views.py

class AirtelPaymentCallbackView(views.APIView):

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction_status = request.data.get('status')

        try:
            transaction = AirtelTransaction.objects.get(transaction_id=transaction_id)
            transaction.status = transaction_status
            transaction.save()

            return Response({'message': 'Transaction status updated successfully'}, status=status.HTTP_200_OK)
        except AirtelTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)


class AirtelPaymentRequestView(views.APIView):

    def post(self, request):
        serializer = AirtelTransactionSerializer(data=request.data)
        if serializer.is_valid():
            # Initiate payment via AirtelMomo API
            airtel_momo = AirtelMomo()
            transaction_id = generate_transaction_id()
            reference = serializer.validated_data['reference']
            msisdn = serializer.validated_data['msisdn']
            amount = serializer.validated_data['amount']
            
            # Call the Airtel Momo API to request payment
            response = airtel_momo.request_payment(
                reference=reference,
                subscriber={"msisdn": msisdn},
                transaction={"amount": amount, "currency": "ZMW", "country": "ZM", "id": transaction_id}
            )
            
            if response['status'] == 'success':
                # Save transaction if successful
                transaction = AirtelTransaction.objects.create(
                    reference=reference,
                    transaction_id=transaction_id,
                    msisdn=msisdn,
                    amount=amount,
                    status='pending'
                )
                return Response({'message': 'Payment request initiated successfully', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to initiate payment'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def get_swagger_file(request):
    base_dir = settings.BASE_DIR
    file_path = os.path.join(base_dir, 'api', 'static', 'api', 'payments-v1.yaml')
    print(file_path)
    
    if os.path.exists(file_path):
        # Return the file as a response
        response = FileResponse(open(file_path, 'rb'), content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment; filename="payments.yaml"'
        return response
    else:
        raise Http404("Swagger file not found")
    

class APILoginView(ObtainAuthToken):
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


class APILogoutView(views.APIView):
    """" Logs out the current signed in user"""

    def get(self, request, format=None):
        """GET request to flash user cookies and log them out"""
        logout(request)
        return Response(status=status.HTTP_200_OK)


class LipilaDisbursementView(viewsets.ModelViewSet):
    """
    API endpoint that allows Disbursments to be viewed and created.
    """
    serializer_class = LipilaDisbursementSerializer
    queryset = LipilaDisbursement.objects.all()
    
    def create(self, request):
        """
        Handles POST requests, deserializing data and updating default fields.
        """
        transaction_id = request.query_params.get('transaction_id')

        if not transaction_id:
            return Response({"error": "reference id is missing"}, status=400)
        try:
            data = request.data
            payee = str(data['send_money_to'])
            amount = str(data['amount'])
            serializer = LipilaDisbursementSerializer(data=data)
            provisioned_mtn_api_user = Disbursement()
            provisioned_mtn_api_user.provision_sandbox(
                provisioned_mtn_api_user.subscription_dis_key, transaction_id)
            provisioned_mtn_api_user.create_api_token(
                provisioned_mtn_api_user.subscription_dis_key, 'disbursement', transaction_id)
            
            if serializer.is_valid():
                request_pay = provisioned_mtn_api_user.deposit(
                    amount=amount, payee=payee, transaction_id=str(transaction_id))
                # save payment object
                api_user = get_user_model().objects.get(pk=1)
                payment = serializer.save()
                payment.api_user = api_user
                payment.updated_at = timezone.now()
                payment.transaction_id = transaction_id

                if request_pay.status_code == 202:
                    
                    payment.status = 'accepted'  # Set status based on mapping
                    payment.save()
                    response = provisioned_mtn_api_user.get_transaction_status('deposit',
                        transaction_id)
                    if response.status_code == 200:
                        payment.status = 'success'
                        payment.save()
                    else:
                        
                        payment.status = 'failed'
                        payment.save()
                    return Response({'message': 'request accepted, wait for client approval'}, status=202)
                elif request_pay.status_code == 403:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Request exceeded'}, status=403)
                elif request_pay.status_code == 400:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Bad request to payment gateway'}, status=400)
            else:
                return Response({'message': 'Data not valid'}, status=400)
        except Exception as e:
            return Response({'message': f'Key Error in submitted data {e}'}, status=400)
        # return Response({'message': 'request accepted, wait for client approval'}, status=202)

    def list(self, request):
        api_user = request.query_params.get('api_user')

        if not api_user:
            return Response({"error": "api user ID is missing"}, status=400)

        user = get_api_user(api_user)
        if isinstance(user, User):
            payments = LipilaDisbursement.objects.filter(api_user=user)
            serializer = LipilaDisbursementSerializer(payments, many=True)
            return Response(serializer.data, status=200)

        return Response({"error": "api user not found"}, status=404)


class LipilaCollectionView(viewsets.ModelViewSet):
    """
    API endpoint that allows COllectins to be viewed and created.
    """
    serializer_class = LipilaCollectionSerializer
    queryset = LipilaCollection.objects.all()

    def create(self, request):
        """
        Handles POST requests, deserializing date and updating default fields.
        """
        transaction_id = request.query_params.get('transaction_id')
        

        if not transaction_id:
            return Response({"error": "reference id is missing"}, status=400)
        
        try:
            data = request.data
            payer = str(data['msisdn'])
            amount = str(data['amount'])
            serializer = LipilaCollectionSerializer(data=data)
            provisioned_mtn_api_user = Collections()
            provisioned_mtn_api_user.provision_sandbox(
                provisioned_mtn_api_user.subscription_col_key, transaction_id)
            provisioned_mtn_api_user.create_api_token(
                provisioned_mtn_api_user.subscription_col_key, 'collection', transaction_id)

            if serializer.is_valid():
                request_pay = provisioned_mtn_api_user.request_to_pay(
                    amount=amount, payer=payer, transaction_id=str(transaction_id))
                # save payment request
                api_user = get_user_model().objects.get(pk=1)
                payment = serializer.save()
                payment.api_user = api_user
                payment.updated_at = timezone.now()
                payment.transaction_id = transaction_id
                if request_pay.status_code == 202:
                    payment.status = 'accepted'  # Set status based on mapping
                    payment.save()
                    # consider makingan an async function call
                    response = provisioned_mtn_api_user.get_payment_status(
                        transaction_id)
                    if response.status_code == 200:
                        payment.status = 'success'
                        payment.save()
                    else:
                        payment.status = 'failed'
                        payment.save()
                    return Response({'message': 'request accepted, wait for client approval'}, status=202)
                elif request_pay.status_code == 403:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Request exceeded'}, status=403)
                elif request_pay.status_code == 400:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Bad request to payment gateway'}, status=400)
            else:
                return Response({'message': 'Data not valid'}, status=400)
        except Exception as e:
            return Response({'message': f'Key Error in submitted data {e}'}, status=400)
        # return Response({'message': 'request accepted, wait for client approval'}, status=202)

    def list(self, request):

        api_user = request.query_params.get('api_user')

        if not api_user:
            return Response({"error": "api user ID is missing"}, status=400)

        user = get_api_user(api_user)
        if isinstance(user, User):
            payments = LipilaCollection.objects.filter(
                api_user=get_api_user(api_user))
            serializer = LipilaCollectionSerializer(payments, many=True)
            return Response(serializer.data, status=200)

        return Response({"error": "api user not found"}, status=404)
