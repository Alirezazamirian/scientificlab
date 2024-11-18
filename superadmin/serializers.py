from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from articles.models import LastArticle
from articles.serializers import SubHeadArticleSerializer, MiddleArticleSerializer
from detail_app.models import Ticket, ContactUs, BlogCategory, Blog
from detail_app.serializers import TicketCategorySerializer


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
    create_at_jalali = serializers.SerializerMethodField(read_only=True)
    update_at_jalali = serializers.SerializerMethodField(read_only=True)
    sub_head_article = serializers.SerializerMethodField(read_only=True)
    middle_article = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LastArticle
        fields = [
            'title',
            'description',
            'abbreviation_name',
            'score',
            'image',
            'sub_head_article',
            'middle_article',
            'create_at_jalali',
            'update_at_jalali',
        ]

    def get_create_at_jalali(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at_jalali(self, obj):
        return obj.get_updated_at_jalali()

    def get_sub_head_article(self, obj):
        if obj.sub_head_article:
            return SubHeadArticleSerializer(obj.sub_head_article, partial=True).data
        return None

    def get_middle_article(self, obj):
        if obj.middle_article:
            return MiddleArticleSerializer(obj.middle_article, partial=True).data
        return None


class ManageTicketsSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    ticket_category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'user',
            'create_at',
            'update_at',
            'ticket_category',
            'is_appropriate',
            'parent',
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_user(self, obj):
        return UserSerializer(obj.user, partial=True).data

    def get_ticket_category(self, obj):
        return TicketCategorySerializer(obj.ticket_category, partial=True).data

    def get_parent(self, obj):
        return ManageTicketsSerializer(obj.parent, partial=True).data


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
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogCategory
        fields = '__all__'

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


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
