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
    date_joined_jalali = serializers.SerializerMethodField(read_only=True)
    last_login_jalali = serializers.SerializerMethodField(read_only=True)
    donate_at_jalali = serializers.SerializerMethodField(read_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'password',
            'new_password',
            'full_name',
            'email',
            'donation',
            'donate_at_jalali',
            'date_joined_jalali',
            'last_login_jalali',
            'branch',
            'degree',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'write_only': True},
            'email': {'required': False, 'read_only': True},
            'phone': {'required': False, 'read_only': True},
            'donation': {'required': False, 'read_only': True},
        }

    def get_date_joined_jalali(self, obj):
        return obj.get_joined_at()

    def get_last_login_jalali(self, obj):
        return obj.get_last_login()

    def get_donate_at_jalali(self, obj):
        return obj.get_donate_at()

class ForgetPassSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, write_only=True)
    code = serializers.IntegerField(required=False, write_only=True)
    password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'code']

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)
        if sum(1 for field in ['email', 'code'] if field in attrs) != 1:
            if 'code' in attrs and 'email' in attrs:
                raise serializers.ValidationError(
                    "Exactly one of the fields 'email' and 'code' must be provided.")
            if 'password' not in attrs or 'confirm_password' not in attrs:
                raise serializers.ValidationError(
                    "Exactly both of the fields 'password' and 'confirm_password' must be provided.")

        if password and confirm_password:
            if len(attrs['confirm_password']) < 8 or len(attrs['password']) < 8:
                return 1
        return attrs
