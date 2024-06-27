import environ
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# My modules
from .serializers import LipilaCollectionSerializer, LipilaDisbursementSerializer
from .models import LipilaCollection, LipilaDisbursement
from api.momo.mtn import Collections, Disbursement
from .helpers import get_api_user

# Define global variables
env = environ.Env()
environ.Env.read_env()
User = get_user_model()


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
        try:
            data = request.data
            payee = str(data['payee_account_number'])
            amount = str(data['amount'])
            serializer = LipilaDisbursementSerializer(data=data)
            provisioned_mtn_api_user = Disbursement()
            provisioned_mtn_api_user.provision_sandbox(
                provisioned_mtn_api_user.subscription_dis_key)
            provisioned_mtn_api_user.create_api_token(
                provisioned_mtn_api_user.subscription_dis_key, 'disbursement')

            if serializer.is_valid():
                reference_id = provisioned_mtn_api_user.x_reference_id
                request_pay = provisioned_mtn_api_user.deposit(
                    amount=amount, payer=payee, reference_id=str(reference_id))
                # save payment object
                api_user = User.objects.get(pk=1)
                payment = serializer.save()
                payment.api_user = api_user
                payment.updated_at = timezone.now()
                payment.reference_id = reference_id

                if request_pay.status_code == 202:
                    payment.status = 'accepted'  # Set status based on mapping
                    payment.save()
                    response = provisioned_mtn_api_user.get_transaction_status('deposit',
                        reference_id)
                    if response.status_code == 200:
                        payment.status = 'success'
                        payment.save()
                    else:
                        payment.status = 'failed'
                        payment.save()
                elif request_pay.status_code == 403:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Request exceeded'}, status=status_code)
                elif request_pay.status_code == 400:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Bad request to payment gateway'}, status=status_code)
        except Exception as e:
            return Response({'message': f'Key Error in submitted data {e}'}, status=400)
        return Response({'message': 'request accepted, wait for client approval'}, status=202)

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
        try:
            data = request.data
            payer = str(data['payer_account_number'])
            amount = str(data['amount'])
            serializer = LipilaCollectionSerializer(data=data)
            provisioned_mtn_api_user = Collections()
            provisioned_mtn_api_user.provision_sandbox(
                provisioned_mtn_api_user.subscription_col_key)
            provisioned_mtn_api_user.create_api_token(
                provisioned_mtn_api_user.subscription_col_key, 'collection')

            if serializer.is_valid():
                reference_id = provisioned_mtn_api_user.x_reference_id
                request_pay = provisioned_mtn_api_user.request_to_pay(
                    amount=amount, payer=payer, reference_id=str(reference_id))
                # save payment request
                api_user = User.objects.get(pk=1)
                payment = serializer.save()
                payment.api_user = api_user
                payment.updated_at = timezone.now()
                payment.reference_id = reference_id
                if request_pay.status_code == 202:
                    payment.status = 'accepted'  # Set status based on mapping
                    payment.save()
                    # consider makingan an async function call
                    response = provisioned_mtn_api_user.get_payment_status(
                        reference_id)
                    if response.status_code == 200:
                        payment.status = 'success'
                        payment.save()
                    else:
                        payment.status = 'failed'
                        payment.save()
                elif request_pay.status_code == 403:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Request exceeded'}, status=status_code)
                elif request_pay.status_code == 400:
                    payment.status = 'failed'
                    payment.save()
                    status_code = request_pay.status_code
                    return Response({'message': 'Bad request to payment gateway'}, status=status_code)
        except Exception as e:
            return Response({'message': f'Key Error in submitted data {e}'}, status=400)
        return Response({'message': 'request accepted, wait for client approval'}, status=202)

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
