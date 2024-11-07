from rest_framework import serializers
from .models import ContactUs, Favorite, Blog, BlogCategory, Star
from accounts.serializers import UserSerializer
from articles.serializers import MiddleArticleSerializer, LastArticleSerializer

class ContactUsSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContactUs
        fields = [
            'create_at',
            'update_at',
            'title',
            'description',
            'answer',
            'is_answered',
            'user',
            'type',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'answer': {'required': False},
            'is_answered': {'required': False},
        }

    def create(self, validated_data):
        user = self.request.user
        validated_data['user'] = user
        contact_us_instance = ContactUs.objects.create(**validated_data)
        return contact_us_instance

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
        return LastArticleSerializer(instance=obj.articles).data


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'required': False, 'read_only': True},
            'article': {'read_only': True, 'required': False},
            'score': {'required': True},
        }

    def validate(self, attr):
        if not attr['score'] <= 5 and attr['score'] >= 1:
            return 1
        else:
            return attr


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogCategory
        fields = '__all__'

    def get_blog(self, obj):
        print(obj)
        blog = Blog.objects.filter(category=obj)
        return BlogSerializer(instance=blog, many=True).data



