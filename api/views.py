import environ
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
import requests
from django.conf import settings

# My modules
from .serializers import MomoColTransactionSerializer, LipilaDisbursementSerializer
from .models import MomoColTransaction, LipilaDisbursement
from .momo.mtn import Collections as MtnMomo
from .momo.mtn import Disbursement
from .utils import get_api_user
from .momo.airtel import AirtelMomo 

# Define global variables
User = get_user_model()


class TransationHistoryView(views.APIView):
    def get(self, request):

        transaction_id = request.query_params.get('transaction_id')

        if not transaction_id:
            return Response({"error": "Transaction_id is missing"}, status=400)

        try:
            payment = MomoColTransaction.objects.get(transaction_id=transaction_id)
            serializer = MomoColTransactionSerializer(payment)
            return Response(serializer.data, status=200)
        except MomoColTransaction.DoesNotExist:
            return Response({"message": "transaction not found"}, status=404)
    

class MtnPaymentCallbackView(views.APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction_status = request.data.get('status')

        try:
            transaction = MomoColTransaction.objects.get(transaction_id=transaction_id)
            transaction.status = transaction_status
            transaction.save()

            return Response({'message': 'Transaction status updated successfully'}, status=status.HTTP_200_OK)
        except MomoColTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)


class MTNPaymentRequestView(views.APIView):

    def post(self, request):
        serializer = MomoColTransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Initiate payment via AirtelMomo API
            transaction_id = serializer.validated_data['transaction_id']
            mtn_api_user = MtnMomo()
            mtn_api_user.provision_sandbox(mtn_api_user.subscription_col_key, transaction_id)
            mtn_api_user.create_api_token(mtn_api_user.subscription_col_key, 'collection', transaction_id)

            reference = serializer.validated_data['reference']
            msisdn = serializer.validated_data['msisdn']
            amount = serializer.validated_data['amount']
            wallet_type = serializer.validated_data['wallet_type']
            
            # Call the Airtel Momo API to request payment
            try:
                response = mtn_api_user.request_to_pay(
                    amount=str(amount),
                    payer=msisdn,
                    transaction_id=transaction_id
                )
                
                # Check if the response is in JSON format
                if response.status_code == 202:
                    try:
                        transaction = MomoColTransaction.objects.create(
                                reference=reference,
                                transaction_id=transaction_id,
                                msisdn=msisdn,
                                amount=amount,
                                status='pending',
                                wallet_type=wallet_type
                            )
                        response = mtn_api_user.get_payment_status(
                            transaction_id)
                        if response.status_code == 200:
                            response_json = response.json()  # Attempt to decode the response
                            if response_json.get('status').lower() == 'successful':
                                transaction.status = 'success'
                                transaction.save()
                                return Response({'message': 'Payment request initiated successfully', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
                            else:
                                transaction.status = 'failed'
                                transaction.save()                            
                                return Response({'message': 'Payment request failed', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({'error': response_json.get('message', 'Failed to initiate payment')}, status=status.HTTP_400_BAD_REQUEST)
                    except ValueError:
                        return Response({'error': 'Invalid JSON response from MTN Momo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'error': f'Failed to initiate payment: Invalid response from MTN Momo: {response.status_code}'}, status=status.HTTP_502_BAD_GATEWAY)

            except requests.RequestException as e:
                return Response({'error': f'Request to MTN Momo API failed: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AirtelPaymentCallbackView(views.APIView):

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction_status = request.data.get('status')

        try:
            transaction = MomoColTransaction.objects.get(transaction_id=transaction_id)
            transaction.status = transaction_status
            transaction.save()

            return Response({'message': 'Transaction status updated successfully'}, status=status.HTTP_200_OK)
        except MomoColTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
    

class AirtelPaymentRequestView(views.APIView):
    
    def post(self, request):
        serializer = MomoColTransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Initiate payment via AirtelMomo API
            airtel_momo = AirtelMomo()
            cleint_id = settings.AIRTEL_CLIENT_ID
            cleint_secret = settings.AIRTEL_CLIENT_SECRET_KEY
            access_token = airtel_momo.authorization(cleint_id, cleint_secret)
            transaction_id = serializer.validated_data['transaction_id']
            reference = serializer.validated_data['reference']
            msisdn = serializer.validated_data['msisdn']
            amount = serializer.validated_data['amount']
            wallet_type = serializer.validated_data['wallet_type']
            
            # Call the Airtel Momo API to request payment
            try:
                response = airtel_momo.request_payment(
                    access_token=access_token,
                    reference=reference,
                    subscriber={"msisdn": msisdn, "country": "ZM", "currency": "ZMW",},
                    transaction={"amount": amount, "currency": "ZMW", "country": "ZM", "id": transaction_id}
                )
                
                # Check if the response is in JSON format
                if response.status_code == 200:
                    try:
                        response_json = response.json()  # Attempt to decode the response
                        if response_json.get('status') == 'success':
                            # Save transaction if successful
                            transaction = MomoColTransaction.objects.create(
                                reference=reference,
                                transaction_id=transaction_id,
                                msisdn=msisdn,
                                amount=amount,
                                status='pending',
                                wallet_type=wallet_type
                            )
                            return Response({'message': 'Payment request initiated successfully', 'transaction': serializer.data}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({'error': response_json.get('message', 'Failed to initiate payment')}, status=status.HTTP_400_BAD_REQUEST)
                    except ValueError:
                        return Response({'error': 'Invalid JSON response from Airtel Momo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'error': 'Failed to initiate payment: Invalid response from Airtel Momo'}, status=status.HTTP_502_BAD_GATEWAY)

            except requests.RequestException as e:
                return Response({'error': f'Request to Airtel Momo API failed: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

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


class MtnDisbursementView(viewsets.ModelViewSet):
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


# class MtnCollectionView(viewsets.ModelViewSet):
#     """
#     API endpoint that allows COllectins to be viewed and created.
#     """
#     serializer_class = MomoColTransactionSerializer
#     queryset = MomoColTransaction.objects.all()

#     def create(self, request):
#         """
#         Handles POST requests, deserializing date and updating default fields.
#         """
#         transaction_id = request.query_params.get('transaction_id')
        

#         if not transaction_id:
#             return Response({"error": "reference id is missing"}, status=400)
        
#         try:
#             data = request.data
#             payer = str(data['msisdn'])
#             amount = str(data['amount'])
#             serializer = MomoColTransactionSerializer(data=data)
#             provisioned_mtn_api_user = MtnMomo()
#             provisioned_mtn_api_user.provision_sandbox(
#                 provisioned_mtn_api_user.subscription_col_key, transaction_id)
#             provisioned_mtn_api_user.create_api_token(
#                 provisioned_mtn_api_user.subscription_col_key, 'collection', transaction_id)

#             if serializer.is_valid():
#                 request_pay = provisioned_mtn_api_user.request_to_pay(
#                     amount=amount, payer=payer, transaction_id=str(transaction_id))
#                 # save payment request
#                 api_user = get_user_model().objects.get(pk=1)
#                 payment = serializer.save()
#                 payment.api_user = api_user
#                 payment.updated_at = timezone.now()
#                 payment.transaction_id = transaction_id
#                 if request_pay.status_code == 202:
#                     payment.status = 'accepted'  # Set status based on mapping
#                     payment.save()
#                     # consider makingan an async function call
#                     response = provisioned_mtn_api_user.get_payment_status(
#                         transaction_id)
#                     if response.status_code == 200:
#                         payment.status = 'success'
#                         payment.save()
#                     else:
#                         payment.status = 'failed'
#                         payment.save()
#                     return Response({'message': 'request accepted, wait for client approval'}, status=202)
#                 elif request_pay.status_code == 403:
#                     payment.status = 'failed'
#                     payment.save()
#                     status_code = request_pay.status_code
#                     return Response({'message': 'Request exceeded'}, status=403)
#                 elif request_pay.status_code == 400:
#                     payment.status = 'failed'
#                     payment.save()
#                     status_code = request_pay.status_code
#                     return Response({'message': 'Bad request to payment gateway'}, status=400)
#             else:
#                 return Response({'message': 'Data not valid'}, status=400)
#         except Exception as e:
#             return Response({'message': f'Key Error in submitted data {e}'}, status=400)
#         # return Response({'message': 'request accepted, wait for client approval'}, status=202)

#     def list(self, request):

#         api_user = request.query_params.get('api_user')

#         if not api_user:
#             return Response({"error": "api user ID is missing"}, status=400)

#         user = get_api_user(api_user)
#         if isinstance(user, User):
#             payments = MomoColTransaction.objects.filter(
#                 api_user=get_api_user(api_user))
#             serializer = MomoColTransactionSerializer(payments, many=True)
#             return Response(serializer.data, status=200)

#         return Response({"error": "api user not found"}, status=404)
