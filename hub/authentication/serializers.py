from django.conf import settings

from rest_framework import serializers


class AuthModelSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name= serializers.CharField(max_length=255)
