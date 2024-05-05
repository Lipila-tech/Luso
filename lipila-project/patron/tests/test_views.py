from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest import mock
# Custom modules


class TestJoinView(TestCase):
    pass