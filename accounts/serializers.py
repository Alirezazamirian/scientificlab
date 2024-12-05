from rest_framework import serializers
from accounts.models import User
from utils.verification import code_expiration


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, write_only=True)
    degree = serializers.CharField(required=False, write_only=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    branch = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'full_name',
            'phone',
            'email',
            'degree',
            'password_confirmation',
            'password',
            'branch'
        ]

    def validate(self, attrs):
        if User.objects.filter(phone=attrs['phone']).exists() or User.objects.filter(email=attrs['email']).exists():
            return 1
        if attrs['password'] != attrs['password_confirmation']:
            return 2
        return attrs


class EmailSerializer(serializers.Serializer):
    verification_code = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        fields = {
            'verification_code',
            'phone'
        }

    def validate(self, attrs):
        if code_expiration(attrs['phone']):
            return 0
        return attrs


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        fields = {
            'password',
            'phone'
        }


class AccountManagementSerializer(serializers.ModelSerializer):
    update_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_update_time(self, obj):
        return obj.update_time