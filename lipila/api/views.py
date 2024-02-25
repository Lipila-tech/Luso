from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import (
    LipilaCollection, Product, MyUser)

from .serializers import UserSerializer
from .serializers import LipilaCollectionSerializer
from .serializers import ProductSerializer, MyUserSerializer

from rest_framework import status
from rest_framework import views, viewsets
from rest_framework.response import Response
from django.shortcuts import render

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.views import APIView
from api.momo.mtn import Collections
from api.helpers import unique_id, apology
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from .forms.forms import DisburseForm


import environ

env = environ.Env()

environ.Env.read_env()

# Django unauthenticated user views


def index(request):
    return render(request, 'UI/index.html')


def service_details(request):
    return render(request, 'UI/services-details.html')


def portfolio_details(request):
    return render(request, 'UI/portfolio-details.html')


def disburse(request):
    """View for the page homapage"""
    context = {}
    context['form'] = DisburseForm()
    return render(request, 'disburse.html', context)

# django authenticated user views


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def dashboard(request, id):
    context = {}
    try:
        # id = int(request.GET.get('user'))
        if not id:
            raise ValueError('User ID missing')
        else:
            user = MyUser.objects.get(id=int(id))
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context)
    except MyUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Not Found!'
        return apology(request, context)
    return render(request, 'AdminUI/index.html', context)


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def users_profile(request, id):
    context = {}
    try:
        # id = int(request.GET.get('user'))
        if not id:
            raise ValueError('User ID missing')
        else:
            user = MyUser.objects.get(id=int(id))
            context['user'] = user
    except ValueError:
        context['status'] = 400
        context['message'] = 'User ID must be of type int'
        return apology(request, context)
    except TypeError:
        context['status'] = 400
        context['message'] = 'Error, User argument missing'
        return apology(request, context)
    except MyUser.DoesNotExist:
        context['status'] = 404
        context['message'] = 'User Profile Not Found!'
        return apology(request, context)
    return render(request, 'AdminUI/users-profile.html', context)


def pages_faq(request):
    return render(request, 'AdminUI/pages-faq.html')


# API Views
User = get_user_model()


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer  # Replace with your serializer

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
            return Response({"Error": 'failed to signup'}, status=400)

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            # Set password, send verification email, etc. (optional)
        except Exception:
            return Response({"Error: Bad Request"}, status=400)

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

class ProductView(viewsets.ModelViewSet):
    """
    Get a users products
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request):
        try:
            username = request.query_params.get('user')

            if not username:
                return Response({"error": "Username is missing"}, status=400)
            else:
                user = User.objects.get(username=username)
                products = Product.objects.filter(product_owner=user.id)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def post(self, request):
        try:
            data = request.data
            serializer = ProductSerializer(data=data)
            return Response({
                'message': "Created",
            }, status=201)
        except Exception:
            return Response({"error: Bad Request"}, status=400)

class LipilaCollectionView(viewsets.ModelViewSet):
    serializer_class = LipilaCollectionSerializer
    queryset = LipilaCollection.objects.all()

    if env("ENV_STATUS") == "offline":
        def create(self, request):
            """No Internet connection, no querying the remote apis"""
            data = request.data
            serializer = LipilaCollectionSerializer(data=data)
            if serializer.is_valid():
                try:
                    # Query external API handlers
                    reference_id = "examplerefernceid"
                    payment = serializer.save()
                    payment.reference_id = reference_id
                    payment.status = 'success'  # Set status to success
                    payment.save()
                    status_code = 200
                    return Response({'message': 'OK'}, status=status_code)
                except Exception as e:
                    return Response({'message': e}, status=400)
            else:
                # Set status code
                return Response({'message': 'Invalid form fields'}, status=405)
    else:
        def create(self, request):
            """Handles POST requests, deserializing date and setting status."""
            data = request.data
            serializer = LipilaCollectionSerializer(data=data)
            api_user = Collections()
            api_user.provision_sandbox(api_user.subscription_col_key)
            api_user.create_api_token(
                api_user.subscription_col_key, 'collection')

            if serializer.is_valid():
                try:
                    # Query external API handlers
                    amount = data['amount']
                    reference_id = api_user.x_reference_id
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


class ProfileView(viewsets.ModelViewSet):
    """Returns the profile of the user"""
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()

    def list(self, request):
        try:
            username = request.query_params.get('user')

            if not username:
                return Response({"Error": "Username is missing"}, status=400)
            else:
                user = MyUser.objects.get(username=username)

            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({"User not found"}, status=404)

    def put(self, request):
        pass
