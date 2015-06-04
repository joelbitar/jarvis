from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout

from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

from authentication.serializers import AuthModelSerializer
from authentication.getauth import GetAuthentication


# Create your views here.
class CurrentUserView(APIView):
    permission_classes = ()

    def get(self, request):
        # If they belong to the hacktivist collective Anonymous
        if request.user.is_anonymous():
            return Response({})

        auth_model_serializer = AuthModelSerializer(request.user)

        return Response(
            auth_model_serializer.data
        )


class LogoutUserView(APIView):
    def post(self, request):
        logout(request)
        return Response({})


class LoginUserView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username']
            )
        except User.DoesNotExist:
            return Response(status=404)

        if not user.check_password(request.data['password']):
            return Response(status=403)

        authentication_backend = settings.AUTHENTICATION_BACKENDS[0]

        user.backend = authentication_backend

        login(request=request, user=user)

        auth_model_serializer = AuthModelSerializer(user)

        return Response(
            auth_model_serializer.data
        )


class AuthenticationViewBaseClass(object):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        GetAuthentication
    )