from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.IntegerField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
