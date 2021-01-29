from django.contrib.auth.models import User
from .models import Balance


class CardNumberAuth(object):
    """
    Auth useing card number from profile
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(balance__card_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
