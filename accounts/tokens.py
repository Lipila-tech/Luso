from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import int_to_base36, base36_to_int
from django.utils.encoding import force_bytes

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.profile.signup_confirmation)
        )

    def _make_token(self, user):
        timestamp = self._num_seconds(self._now())
        hash_value = self._make_hash_value(user, timestamp)
        return self._make_token_with_timestamp(user, timestamp, hash_value)

    def _make_token_with_timestamp(self, user, timestamp, hash_value):
        ts_b36 = int_to_base36(timestamp)
        return f"{hash_value}-{ts_b36}"

account_activation_token = AccountActivationTokenGenerator()
