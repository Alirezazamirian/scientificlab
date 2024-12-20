from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AdminTicket
from scientificlab.settings import EMAIL_HOST_USER
from .serializers import (ManageUserSerializer, ManageArticleSerializer, ManageTicketsSerializer,
                          ManageContactUsSerializer, ManageBlogCategorySerializer, ManageBlogSerializer,
                          ManageSubArticlesSerializer, ManageMiddleArticlesSerializer, ManageHeadArticlesSerializer,
                          ManageLastArticlesSerializer, ManageImageArticleSerializer, ManageDescriptionArticleSerializer,
                          ManageAdminTicketSerializer)
from .permissions import IsSuperAndStuffUser
from accounts.models import User
from articles.models import LastArticle, SubHeadArticle, MiddleArticle, HeadArticle, ArticleImages, ArticleDescription
from detail_app.models import Ticket, ContactUs, Blog, BlogCategory
from django.core.mail import send_mail
import datetime


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
    http_method_names = ['get',]

    def list(self, request, *args, **kwargs):
        ticket_category = self.request.query_params.get('ticket_category', None)
        not_answered_ticket = self.queryset.filter(is_answered=False).count()
        if ticket_category:
            ser = self.serializer_class(self.queryset.filter(ticket_category=ticket_category), many=True)
        else:
            ser = self.serializer_class(self.queryset, many=True)
        return Response({'result': ser.data, 'not_answered_count': not_answered_ticket}, status=status.HTTP_200_OK)

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

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False, is_active=True)

    def get(self, request):
        users = self.get_queryset()
        users_count = users.count()
        users_paid_count = users.filter(is_pay=True).count()
        x = 0
        for user in users:
            x += user.donation
        return Response(data={'paid_users_count': users_paid_count,
                              'full_donation': x,
                              'users_count': users_count}, status=status.HTTP_200_OK)


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


class UserBranchCount(APIView):
    permission_classes = (IsSuperAndStuffUser, )

    def get(self, request):
        users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
        MD_count = 0
        dentist_count = 0
        lab_science_count = 0
        paramedical_count = 0
        nurse_count = 0
        high_educated_MD_count = 0
        other_count = 0
        for user in users:
            if user.branch == 'MD':
                MD_count += 1
            elif user.branch == 'dentist':
                dentist_count += 1
            elif user.branch == 'lab_science':
                lab_science_count += 1
            elif user.branch == 'paramedical':
                paramedical_count += 1
            elif user.branch == 'nurse':
                nurse_count += 1
            elif user.branch == 'HMD':
                high_educated_MD_count += 1
            else:
                other_count += 1
        return Response({
            'MD_count': MD_count,
            'dentist_count': dentist_count,
            'lab_science_count': lab_science_count,
            'paramedical_count': paramedical_count,
            'nurse_count': nurse_count,
            'high_educated_MD_count': high_educated_MD_count,
            'other_count': other_count
        }, status=status.HTTP_200_OK)


class ManageAdminTickets(viewsets.ModelViewSet):
    queryset = AdminTicket.objects.all()
    serializer_class = ManageAdminTicketSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        ticket_category = self.request.query_params.get('ticket_category', None)
        if ticket_category:
            ser = self.serializer_class(self.queryset.filter(ticket__ticket_category=ticket_category), many=True)
        else:
            ser = self.serializer_class(self.queryset, many=True)
        return Response({ser.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            user_ticket = ser.validated_data['ticket']
            Ticket.objects.filter(id=user_ticket).update(is_answered=True)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        ticket = self.get_object()
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ticket.status = ser.validated_data['status']
            ticket.description = ser.validated_data['description']
            ticket.ticket.id = ser.validated_data['ticket']
            ticket.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        ticket = self.get_object()
        ser = self.serializer_class(ticket, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class UserPaymentDate(APIView):
    permission_classes = (IsSuperAndStuffUser,)

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False, is_active=True, is_pay=True)

    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        now = datetime.datetime.now()
        one_month_ago = now - datetime.timedelta(days=30)
        three_month_ago = now - datetime.timedelta(days=90)
        six_month_ago = now - datetime.timedelta(days=180)
        one_year_ago = now - datetime.timedelta(days=365)
        in_one_month = 0
        in_three_month = 0
        in_six_month = 0
        in_one_year = 0
        befor_year = 0
        for user in query:
            aware_user_tz = user.pay_at.replace(tzinfo=None)
            if aware_user_tz > one_month_ago:
                in_one_month += 1
            elif aware_user_tz > three_month_ago and aware_user_tz < one_year_ago:
                in_three_month += 1
            elif aware_user_tz > six_month_ago and aware_user_tz < three_month_ago:
                in_six_month += 1
            elif aware_user_tz > one_year_ago and aware_user_tz < six_month_ago:
                in_one_year += 1
            else:
                befor_year += 1
        return Response({
            'in_one_month': in_one_month,
            'in_three_month': in_three_month,
            'in_six_month': in_six_month,
            'in_one_year': in_one_year,
            'befor_year': befor_year,
        }, status=status.HTTP_200_OK)