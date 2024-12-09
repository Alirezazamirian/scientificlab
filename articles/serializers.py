from rest_framework import serializers
from .models import HeadArticle, SubHeadArticle, MiddleArticle, LastArticle, ArticleDescription, ArticleImages


class HeadArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = HeadArticle
        exclude = ['updated_at', 'id']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class SubHeadArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    head_article = serializers.SerializerMethodField()

    class Meta:
        model = SubHeadArticle
        exclude = ['updated_at', 'id']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_head_article(self, obj):
        return HeadArticleSerializer(obj.head_article).data


class MiddleArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    sub_head_article = serializers.SerializerMethodField()

    class Meta:
        model = MiddleArticle
        exclude = ['updated_at', 'id']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_sub_head_article(self, obj):
        return SubHeadArticleSerializer(obj.sub_head_article).data


class ArticleImagesSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = ArticleImages
        exclude = ['updated_at', 'id', 'article']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ArticleDescriptionSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ArticleDescription
        exclude = ['updated_at', 'id', 'article']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_image(self, obj):
        if obj.image:
            return ArticleImagesSerializer(obj.image).data


class LastArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    sub_head_article = serializers.SerializerMethodField()
    middle_article = serializers.SerializerMethodField()
    seperated_description = serializers.SerializerMethodField()

    class Meta:
        model = LastArticle
        exclude = ['updated_at', 'id']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_sub_head_article(self, obj):
        if obj.sub_head_article:
            return SubHeadArticleSerializer(obj.sub_head_article).data

    def get_middle_article(self, obj):
        if obj.middle_article:
            return MiddleArticleSerializer(obj.middle_article).data

    def get_seperated_description(self, obj):
        return ArticleDescriptionSerializer(ArticleDescription.objects.filter(article=obj), many=True).data

