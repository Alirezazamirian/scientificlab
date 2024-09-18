from rest_framework import serializers
from .models import ContactUs, Favorite, Blog, BlogCategory
from accounts.serializers import UserSerializer
from articles.serializers import MiddleArticleSerializer, LastArticleSerializer

class ContactUsSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = ContactUs
        excludes = ['updated_at']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = '__all__'
        # exclude = ['articles']

    def get_user(self, obj):
        return UserSerializer(instance=obj.user).data

    def get_articles(self, obj):
        return LastArticleSerializer(instance=obj.articles, many=True).data
