from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import HeadArticle, SubHeadArticle, MiddleArticle, LastArticle, ArticleDescription, ArticleImages, HeadArticleImages


class HeadArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    sub_test = serializers.SerializerMethodField()
    sub_experiment = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = HeadArticle
        fields = [
            'title',
            'description',
            'create_at',
            'update_at',
            'image',
            'sub_test',
            'sub_experiment',
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context')
        self.request = request.get('request')
        super().__init__(*args, **kwargs)

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_sub_test(self, obj):
        sub_test = SubHeadArticle.objects.filter(head_article=obj, type='Test')
        return SubHeadArticleSerializer(sub_test, many=True, context={'request': self.request}).data

    def get_sub_experiment(self, obj):
        sub_experiment = SubHeadArticle.objects.filter(head_article=obj, type='Experiment')
        return SubHeadArticleSerializer(sub_experiment, many=True, context={'request': self.request}).data

    def get_image(self, obj):
        image = HeadArticleImages.objects.filter(head_article=obj).first()
        return HeadArticleImagesSerializer(image, partial=True).data


class SubHeadArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    middle_article = serializers.SerializerMethodField()
    last_article = serializers.SerializerMethodField()

    class Meta:
        model = SubHeadArticle
        exclude = ['updated_at', 'id']

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context')
        self.request = request.get('request')
        super().__init__(*args, **kwargs)

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_middle_article(self, obj):
        middle_article = MiddleArticle.objects.filter(sub_head_article=obj)
        return MiddleArticleSerializer(middle_article, many=True, context={'request': self.request}).data

    def get_last_article(self, obj):
        last_article = LastArticle.objects.filter(sub_head_article=obj)
        for article in last_article:
            if article.is_free or (not article.is_free and self.request.user.is_pay):
                return LastArticleSerializer(last_article, many=True, context={'request': self.request}).data
            else:
                return {'error': 'payment error!'}

class MiddleArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    last_article = serializers.SerializerMethodField()

    class Meta:
        model = MiddleArticle
        exclude = ['updated_at', 'id']

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context')
        self.request = request.get('request')
        super().__init__(*args, **kwargs)

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_last_article(self, obj):
        last_article = LastArticle.objects.filter(middle_article=obj)
        for article in last_article:
            if article.is_free or (not article.is_free and self.request.user.is_pay):
                return LastArticleSerializer(last_article, many=True, context={'request': self.request}).data
            else:
                return {'error': 'payment error!'}


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

class HeadArticleImagesSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = HeadArticleImages
        exclude = ['updated_at', 'id', 'head_article']

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
    seperated_description = serializers.SerializerMethodField()

    class Meta:
        model = LastArticle
        exclude = ['updated_at', 'id']

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context')
        self.request = request.get('request')
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        if attrs.is_free or (not attrs.is_free and self.request.user.is_pay):
            pass
        else:
            return ValidationError({'error': 'you are not able to see this doc'})
    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_seperated_description(self, obj):
        return ArticleDescriptionSerializer(ArticleDescription.objects.filter(article=obj), many=True).data

