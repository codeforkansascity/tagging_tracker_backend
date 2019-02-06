from rest_framework import serializers


class TokenValidator(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
