from rest_framework import serializers
from .models import HeadArticle, SubHeadArticle, MiddleArticle, LastArticle
from detail_app.models import Star


class HeadArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = HeadArticle
        exclude = ['updated_at']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class SubHeadArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = SubHeadArticle
        exclude = ['updated_at']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class MiddleArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()
    allscore = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MiddleArticle
        exclude = ['updated_at']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_allscore(self, obj):
        all_score = Star.objects.filter(article=obj)
        all_star = 0
        for star in all_score:
            all_star += star.score
        all_star = all_star / all_score.count()
        return all_star

class LastArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = LastArticle
        exclude = ['updated_at']

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()
