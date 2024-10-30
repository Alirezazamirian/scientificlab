from rest_framework import serializers
from accounts.models import User


class ManageUserSerializer(serializers.ModelSerializer):
    date_joined_jalali = serializers.SerializerMethodField(read_only=True)
    last_login_jalali = serializers.SerializerMethodField(read_only=True)
    donate_at_jalali = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'is_pay',
            'donation',
            'donate_at_jalali',
            'is_active',
            'date_joined_jalali',
            'last_login_jalali',
            'branch',
            'degree',
            'is_superuser'
        ]

    def get_date_joined_jalali(self, obj):
        return obj.get_joined_at()

    def get_last_login_jalali(self, obj):
        return obj.get_last_login()

    def get_donate_at_jalali(self, obj):
        return obj.get_donate_at()

