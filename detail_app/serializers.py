from rest_framework import serializers
from .models import ContactUs, Favorite, Blog, BlogCategory, Star, TicketCategory, Ticket, TicketConversation
from accounts.serializers import UserSerializer
from articles.serializers import MiddleArticleSerializer, LastArticleSerializer
from superadmin.models import AdminTicket

class AdminTicketSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AdminTicket
        fields = [
            'create_at',
            'update_at',
            'description'
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.method == 'POST':
            self.fields['title'].required = True
            self.fields['description'].required = True
            self.fields['answer'].required = False
            self.fields['is_answered'].required = False
            self.fields['type'].required = True
        if request and request.method in ['PUT', 'PATCH']:
            self.fields['title'].required = False
            self.fields['description'].required = False
            self.fields['answer'].required = True
            self.fields['is_answered'].required = True
            self.fields['type'].required = False

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class FavouriteSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    article_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'
        extra_kwargs = {
            'article_id': {'write_only': True, 'required': True},
            'user': {'required': False},
            'articles': {'read_only': True}
        }

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
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'title',
            'description',
            'image',
            'category',
            'create_at',
            'update_at',
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()


class BlogCategorySerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogCategory
        exclude = [
            'id',
        ]

    def get_blog(self, obj):
        blog = Blog.objects.filter(category=obj)
        return BlogSerializer(instance=blog, many=True).data


class TicketCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketCategory
        fields = [
            'type'
        ]


class TicketSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)
    admin_ticket = serializers.SerializerMethodField(read_only=True)
    ticket_category = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = [
            'update_at',
            'create_at',
            'ticket_category',
            'admin_ticket',
            'description',
            'title',
            'id',
            'is_answered'
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_admin_ticket(self, obj):
        admin_ticket = AdminTicket.objects.filter(ticket=obj)
        if admin_ticket.exists():
            for admin in admin_ticket:
                return AdminTicketSerializer(instance=admin).data
        else:
            return None

class TicketConversationSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField(read_only=True)
    update_at = serializers.SerializerMethodField(read_only=True)
    ticket_category = serializers.SerializerMethodField(read_only=True)
    ticket = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = TicketConversation
        fields = [
            'id',
            'create_at',
            'update_at',
            'ticket_category',
            'ticket'
        ]

    def get_create_at(self, obj):
        return obj.get_create_at_jalali()

    def get_update_at(self, obj):
        return obj.get_updated_at_jalali()

    def get_ticket_category(self, obj):
        return TicketCategorySerializer(instance=obj.ticket.ticket_category, partial=True).data

    def get_ticket(self, obj):
        return TicketSerializer(instance=obj.ticket, partial=True).data


class DonationSerializer(serializers.Serializer):
    donation = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        donation = attrs.get('donation', None)
        if donation and type(donation) == int and donation > 1001:
            return attrs
        else:
            raise serializers.ValidationError('donation has to be int and greater than 1001 toman!')
