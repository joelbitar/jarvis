from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User


class AuthTokenSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.key

class AuthModelSerializer(serializers.Serializer):
    auth_token = AuthTokenSerializer(read_only=True)
    pk = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

