from rest_framework import serializers
from accounts.models import User
from utils.verification import code_expiration

DEGREE = ['پزشکی', 'دیپلم', 'کارشناسی', 'کارشناسی ارشد', 'دکتری']


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    degree = serializers.CharField(required=False)
    password_confirmation = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    branch = serializers.CharField(required=False)

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
        if attrs['degree'] not in DEGREE:
            return 3
        if attrs['full_name'].split(' ').__len__() <= 1:
            return 4
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
