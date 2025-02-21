from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from articles.models import LastArticle, SubHeadArticle, MiddleArticle, HeadArticle, ArticleImages, ArticleDescription
from articles.serializers import ArticleDescriptionSerializer
from detail_app.models import Ticket, ContactUs, BlogCategory, Blog, TicketConversation, TicketCategory
from .models import AdminTicket
from detail_app.serializers import TicketSerializer


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


class ManageArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)
    sub_head_article = serializers.SerializerMethodField(read_only=True)
    middle_article = serializers.SerializerMethodField(read_only=True)
    head_article = serializers.SerializerMethodField(read_only=True)
    seperated_description = serializers.SerializerMethodField()

    class Meta:
        model = LastArticle
        exclude = [
            'updated_at'
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_sub_head_article(self, obj):
        if obj.sub_head_article:
            return ManageSubArticlesSerializer(obj.sub_head_article, partial=True).data
        return None

    def get_middle_article(self, obj):
        if obj.middle_article:
            return ManageMiddleArticlesSerializer(obj.middle_article, partial=True).data
        return None

    def get_head_article(self, obj):
        if obj.middle_article:
            return ManageHeadArticlesSerializer(obj.middle_article.sub_head_article.head_article, partial=True).data
        if obj.sub_head_article:
            return ManageHeadArticlesSerializer(obj.sub_head_article.head_article, partial=True).data
        return None

    def get_seperated_description(self, obj):
        return ArticleDescriptionSerializer(ArticleDescription.objects.filter(article=obj), many=True).data


class ManageSubArticlesSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = SubHeadArticle
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageHeadArticlesSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = HeadArticle
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageMiddleArticlesSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = MiddleArticle
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageLastArticlesSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = LastArticle
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageTicketsSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    ticket = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TicketConversation
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_user(self, obj):
        return ManageUserSerializer(obj.user).data

    def get_ticket(self, obj):
        return TicketSerializer(obj.ticket, partial=True).data


class ManageContactUsSerializer(serializers.ModelSerializer):
    create_at_jalali = serializers.SerializerMethodField(read_only=True)
    update_at_jalali = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContactUs
        exclude = [
            'create_at',
            'updated_at'
        ]

    def __init__(self, *args, **kwargs):
        super(ManageContactUsSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ['PUT']:
                self.fields.get('is_answered').required = True
                self.fields.get('answer').required = True
                self.fields.get('title').required = False
                self.fields.get('description').required = False
                self.fields.get('type').required = False
                self.fields.get('user').required = False

    def get_create_at_jalali(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at_jalali(self, obj):
        return obj.get_updated_at_jalali()

    def get_user(self, obj):
        return ManageUserSerializer(obj.user, partial=True).data


class ManageBlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'


class ManageBlogSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageDescriptionArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = ArticleDescription
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageImageArticleSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    update_at = serializers.SerializerMethodField()

    class Meta:
        model = ArticleImages
        exclude = ['updated_at', ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class ManageAdminTicketSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AdminTicket
        fields = [
            'create_at',
            'update_at',
            'ticket',
            'description',
            'status'
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_ticket(self, obj):
        return TicketSerializer(obj.ticket, partial=True).data


class ManageAdminTicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = '__all__'
