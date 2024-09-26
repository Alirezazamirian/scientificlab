from rest_framework import serializers

from accounts.models import User


class ManageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'