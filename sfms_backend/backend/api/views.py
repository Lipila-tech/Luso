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


# Create your views here.
class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

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