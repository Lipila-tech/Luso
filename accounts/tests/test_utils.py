from django.test import TestCase
from django.conf import settings
from accounts.utils import basic_auth_encode, is_base64, basic_auth_decode
from django.contrib.auth import get_user_model


class BasicAuthTest(TestCase):
    def test_basic_auth_encode(self):
        user = get_user_model().objects.create(username='test_user', password='test_pass')
        b64 = basic_auth_encode(user.pk)
        self.assertTrue(b64, is_base64(b64))

    def test_basic_auth_decode(self):
        user = get_user_model().objects.create(username='test_user', password='test_pass')
        b64 = basic_auth_encode(user.pk)
        b64_to_str = basic_auth_decode(b64)
        self.assertFalse(is_base64(b64_to_str), False)
        self.assertEqual((b64_to_str), user.pk)
