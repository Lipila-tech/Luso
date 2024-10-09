from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class SocialAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, **kwargs):
        try:
            # Get the user by their TikTok username
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, **kwargs):
        UserModel = User
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        UserModel = User
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = User
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # Allow authentication with email or username
            user = UserModel.objects.get(
                models.Q(username__iexact=username) | models.Q(
                    email__iexact=username)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
