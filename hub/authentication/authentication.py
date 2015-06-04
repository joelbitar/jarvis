__author__ = 'joel'

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class GetAuthentication(TokenAuthentication):
    def authenticate(self, request):
        key = request.GET.get('token', None)

        if key is None:
            raise AuthenticationFailed('Invalid GET string, no token param')

        return self.authenticate_credentials(key)

