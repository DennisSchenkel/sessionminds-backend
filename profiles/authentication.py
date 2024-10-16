from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework import exceptions


# Custom JWT authentication class
class CustomJWTAuthentication(JWTAuthentication):
    """
        A custom JWT authentication class.

    Args:
        JWTAuthentication: Inherits from JWTAuthentication class.
    """
    # Override the get_validated_token method
    def get_validated_token(self, raw_token):
        # Check if token is blacklisted
        if isinstance(raw_token,
                      str
                      ) and BlacklistedToken.objects.filter(
                          token=raw_token).exists():
            raise exceptions.AuthenticationFailed("Token is blacklisted.")

        # Give the token to the parent class
        return super().get_validated_token(raw_token)
