from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from scientificlab.settings import EMAIL_HOST_USER
from .serializers import (ManageUserSerializer, ManageArticleSerializer, ManageTicketsSerializer,
                          ManageContactUsSerializer, ManageBlogCategorySerializer, ManageBlogSerializer,
                          ManageSubArticlesSerializer, ManageMiddleArticlesSerializer, ManageHeadArticlesSerializer,
                          ManageLastArticlesSerializer, ManageImageArticleSerializer, ManageDescriptionArticleSerializer)
from .permissions import IsSuperAndStuffUser
from accounts.models import User
from articles.models import LastArticle, SubHeadArticle, MiddleArticle, HeadArticle, ArticleImages, ArticleDescription
from detail_app.models import Ticket, ContactUs, Blog, BlogCategory
from django.core.mail import send_mail


class ManageUsers(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False, is_staff=False)
    serializer_class = ManageUserSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put', ]

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        ser = self.serializer_class(user, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        ser = self.serializer_class(user, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ManageAllArticles(viewsets.ModelViewSet):
    queryset = LastArticle.objects.all()
    serializer_class = ManageArticleSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get',]

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        article = self.get_object()
        ser = self.serializer_class(article, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ManageSubArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageSubArticlesSerializer
    queryset = SubHeadArticle.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        sub_article = self.get_object()
        ser = self.serializer_class(sub_article, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageMiddleArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageMiddleArticlesSerializer
    queryset = MiddleArticle.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        middle_article = self.get_object()
        ser = self.serializer_class(middle_article, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageHeadArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageHeadArticlesSerializer
    queryset = HeadArticle.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        head_article = self.get_object()
        ser = self.serializer_class(head_article, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageLastArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageLastArticlesSerializer
    queryset = LastArticle.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        last_article = self.get_object()
        ser = self.serializer_class(last_article, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageTickets(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = ManageTicketsSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put',]

    def list(self, request, *args, **kwargs):
        ticket_category = self.request.query_params.get('ticket_category', None)
        ser = self.serializer_class(self.queryset.filter(ticket_category=ticket_category), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        ticket = self.get_object()
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            Ticket.objects.create(
                parent_id=ticket.id,
                title=ser.data['title'],
                description=ser.data['description'],
                user_id=self.request.user.id,
                ticket_category=kwargs['ticket_category'],
                is_appropriate=True,
            )
            ticket.is_appropriate = True
            ticket.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        ticket = self.get_object()
        ser = self.serializer_class(ticket, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ManageContactUs(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ManageContactUsSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put', ]

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        contact_us = self.get_object()
        ser = self.serializer_class(contact_us, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            if contact_us.is_answered:
                send_mail("subject", f"your answer is : {contact_us.answer}", EMAIL_HOST_USER, [contact_us.user.email])
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        contact_us = self.get_object()
        ser = self.serializer_class(contact_us, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class UserPayment(APIView):
    permission_classes = (IsSuperAndStuffUser,)
    queryset = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)

    def get(self, request):
        users_count = self.queryset.count()
        users_paid_count = self.queryset.filter(is_paid=True).count()
        x = 0
        for payment in self.queryset:
            x += payment.donation
        return Response(data={'paid_users_count': users_paid_count,
                              'full_donation': x,
                              'not_paid_users_count': users_count - users_paid_count}, status=status.HTTP_200_OK)


class ManageCategoryBlog(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = ManageBlogCategorySerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        blog_cat = self.get_object()
        ser = self.serializer_class(blog_cat, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        blog_cat = self.get_object()
        ser = self.serializer_class(blog_cat, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ManageBlog(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = ManageBlogSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        blog = self.get_object()
        ser = self.serializer_class(blog, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        blog = self.get_object()
        ser = self.serializer_class(blog, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ManageDescriptionArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageDescriptionArticleSerializer
    queryset = ArticleDescription.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        last_article = self.get_object()
        ser = self.serializer_class(last_article, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageImageArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageImageArticleSerializer
    queryset = ArticleImages.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        last_article = self.get_object()
        ser = self.serializer_class(last_article, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

