from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from detail_app.serializers import ContactUsSerializer
from .models import AdminTicket
from scientificlab.settings import EMAIL_HOST_USER
from .serializers import (ManageUserSerializer, ManageArticleSerializer, ManageTicketsSerializer,
                          ManageContactUsSerializer, ManageBlogCategorySerializer, ManageBlogSerializer,
                          ManageSubArticlesSerializer, ManageMiddleArticlesSerializer, ManageHeadArticlesSerializer,
                          ManageLastArticlesSerializer, ManageImageArticleSerializer, ManageDescriptionArticleSerializer,
                          ManageAdminTicketSerializer, ManageAdminTicketCategorySerializer)
from .permissions import IsSuperAndStuffUser
from accounts.models import User
from articles.models import LastArticle, SubHeadArticle, MiddleArticle, HeadArticle, ArticleImages, ArticleDescription
from detail_app.models import Ticket, ContactUs, Blog, BlogCategory, TicketConversation, TicketCategory
from django.core.mail import send_mail
import datetime
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


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


# only for GET method in admin panel
class ManageAllArticles(viewsets.ModelViewSet):
    queryset = LastArticle.objects.all()
    serializer_class = ManageArticleSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get',]

    def list(self, request, *args, **kwargs):
        queryset = LastArticle.objects.all()
        ser = self.serializer_class(queryset, many=True)
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
        queryset = SubHeadArticle.objects.all()
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            head_article = HeadArticle.objects.filter(id=ser.validated_data.get('head_article_id', None)).first()
            if not head_article:
                return Response(data={'result': 'there is no Head Article with this ID'}, status=status.HTTP_400_BAD_REQUEST)
            SubHeadArticle.objects.create(title=ser.validated_data.get('title', None),
                                          description=ser.validated_data.get('description', None),
                                          type=ser.validated_data.get('type', None),
                                          head_article=head_article,
                                          slug=ser.validated_data.get('slug', None))
            return Response(data={'result': 'created successfully'}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        sub_article = self.get_object()
        ser = self.serializer_class(sub_article, data=request.data, partial=True)
        if ser.is_valid():
            head_article = HeadArticle.objects.get(id=ser.validated_data.get('head_article_id', None))
            ser.head_article = head_article
            ser.title = ser.validated_data.get('title', None)
            ser.description = ser.validated_data.get('description', None)
            ser.type = ser.validated_data.get('type', None)
            ser.slug = ser.validated_data.get('slug', None)
            ser.save()
            return Response(data={'result': 'updated successfully'}, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageMiddleArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageMiddleArticlesSerializer
    queryset = MiddleArticle.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = MiddleArticle.objects.all()
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            sub_head_article = SubHeadArticle.objects.filter(id=ser.validated_data.get('sub_head_article_id', None)).first()
            if not sub_head_article:
                return Response(data={'result': 'there is no Sub Head Article with this ID'}, status=status.HTTP_400_BAD_REQUEST)
            MiddleArticle.objects.create(title=ser.validated_data.get('title', None),
                                         description=ser.validated_data.get('description', None),
                                         sub_head_article=sub_head_article,
                                         slug=ser.validated_data.get('slug', None))
            return Response(data={'result': 'created successfully'}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        middle_article = self.get_object()
        ser = self.serializer_class(middle_article, data=request.data, partial=True)
        if ser.is_valid():
            sub_head_article = SubHeadArticle.objects.filter(
                id=ser.validated_data.get('sub_head_article_id', None)).first()
            if not sub_head_article:
                return Response(data={'result': 'there is no Sub Head Article with this ID'},
                                status=status.HTTP_400_BAD_REQUEST)
            ser.head_article = sub_head_article
            ser.title = ser.validated_data.get('title', None)
            ser.description = ser.validated_data.get('description', None)
            ser.slug = ser.validated_data.get('slug', None)
            ser.save()
            return Response(data={'result': 'updated successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageHeadArticles(viewsets.ModelViewSet):
    permission_classes = (IsSuperAndStuffUser,)
    serializer_class = ManageHeadArticlesSerializer
    queryset = HeadArticle.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = HeadArticle.objects.all()
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
        queryset = LastArticle.objects.all()
        ser = self.serializer_class(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            sub_head_article = SubHeadArticle.objects.filter(
                id=ser.validated_data.get('sub_head_article_id', None)).first()
            if not sub_head_article and ser.validated_data.get('sub_head_article_id', None):
                return Response(data={'result': 'there is no Sub Head Article with this ID'},
                                status=status.HTTP_400_BAD_REQUEST)

            middle_article = MiddleArticle.objects.filter(
                id=ser.validated_data.get('middle_article_id', None)).first()
            if not middle_article and ser.validated_data.get('middle_article_id', None):
                return Response(data={'result': 'there is no Middle Article with this ID'},
                                status=status.HTTP_400_BAD_REQUEST)

            LastArticle.objects.create(title=ser.validated_data.get('title', None),
                                       description=ser.validated_data.get('description', None),
                                       sub_head_article=sub_head_article,
                                       middle_article=middle_article,
                                       slug=ser.validated_data.get('slug', None),
                                       abbreviation_name=ser.validated_data.get('abbreviation_name', None),
                                       score=ser.validated_data.get('score', None),
                                       is_free=ser.validated_data.get('is_free', None),)

            return Response(data={'result': 'created successfully'}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        last_article = self.get_object()
        ser = self.serializer_class(last_article, data=request.data, partial=True)
        if ser.is_valid():
            sub_head_article = SubHeadArticle.objects.filter(
                id=ser.validated_data.get('sub_head_article_id', None)).first()
            if not sub_head_article and ser.validated_data.get('sub_head_article_id', None):
                return Response(data={'result': 'there is no Sub Head Article with this ID'},
                                status=status.HTTP_400_BAD_REQUEST)

            middle_article = MiddleArticle.objects.filter(
                id=ser.validated_data.get('middle_article_id', None)).first()
            if not middle_article and ser.validated_data.get('middle_article_id', None):
                return Response(data={'result': 'there is no Middle Article with this ID'},
                                status=status.HTTP_400_BAD_REQUEST)

            ser.title = ser.validated_data.get('title', None)
            ser.description = ser.validated_data.get('description', None)
            ser.score = last_article.score
            ser.is_free = ser.validated_data.get('is_free', None)
            ser.abbreviation_name = ser.validated_data.get('abbreviation_name', None)
            ser.slug = ser.validated_data.get('slug', None)
            ser.sub_head_article = sub_head_article
            ser.middle_article = middle_article
            ser.save()
            return Response(data={'result': 'updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageTickets(viewsets.ModelViewSet):
    queryset = TicketConversation.objects.all()
    serializer_class = ManageTicketsSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get',]

    def list(self, request, *args, **kwargs):
        ticket_category = self.request.query_params.get('ticket_category', None)
        not_answered_ticket = self.queryset.filter(ticket__is_answered=False).count()
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
    serializer_class = ContactUsSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put', ]

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(ContactUs.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        contact_us = self.get_object()
        ser = self.serializer_class(contact_us, data=request.data, partial=True)
        if ser.is_valid():
            contact_us.answer = ser.validated_data['answer']
            contact_us.is_answered = ser.validated_data['is_answered']
            contact_us.save()
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
        ser = self.serializer_class(BlogCategory.objects.all(), many=True)
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
        ser = self.serializer_class(Blog.objects.all(), many=True)
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
        return Response(data=ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data, partial=True)
        if ser.is_valid():
            user_ticket = ser.validated_data.get('ticket', None)
            if user_ticket is None:
                return Response({'Error': 'Ticket must be provided'}, status=status.HTTP_400_BAD_REQUEST)
            Ticket.objects.filter(id=user_ticket.id).update(is_answered=True)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        ticket = self.get_object()
        ser = self.serializer_class(ticket, data=request.data, partial=True)
        if ser.is_valid():
            ticket_status = ser.validated_data.get('status', None)
            ticket_description = ser.validated_data.get('description', None)
            ticket_ticket = ser.validated_data.get('ticket', None)
            ticket.status = ticket_status if ticket_status is not None else True
            ticket.description = ticket_description if ticket_description is not None else ticket.description
            ticket.ticket.id = ticket_ticket if ticket_ticket is not None else ticket.ticket.id
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


@method_decorator(never_cache, name='dispatch')
class UserDonations(APIView):
    permission_classes = (IsSuperAndStuffUser,)

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False, is_active=True, donation__gt=0)

    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        if not query:
            return Response(data={'error': 'No one has donated yet!'}, status=status.HTTP_204_NO_CONTENT)
        now = datetime.datetime.now()
        one_month_ago = now - datetime.timedelta(days=30)
        three_month_ago = now - datetime.timedelta(days=90)
        six_month_ago = now - datetime.timedelta(days=180)
        one_year_ago = now - datetime.timedelta(days=365)
        in_one_month = 0
        in_one_month_amount = 0
        in_three_month = 0
        in_three_month_amount = 0
        in_six_month = 0
        in_six_month_amount = 0
        in_one_year = 0
        in_one_year_amount = 0
        befor_year = 0
        befor_year_amount = 0
        for user in query:
            aware_user_tz = user.donate_at.replace(tzinfo=None)
            if aware_user_tz > one_month_ago:
                in_one_month += 1
                in_one_month_amount += user.donation
            elif aware_user_tz > three_month_ago and aware_user_tz < one_year_ago:
                in_three_month += 1
                in_three_month_amount += user.donation
            elif aware_user_tz > six_month_ago and aware_user_tz < three_month_ago:
                in_six_month += 1
                in_six_month_amount += user.donation
            elif aware_user_tz > one_year_ago and aware_user_tz < six_month_ago:
                in_one_year += 1
                in_one_year_amount += user.donation
            else:
                befor_year += 1
                befor_year_amount += user.donation
        return Response(data={
            'count': {
                'in_one_month': in_one_month,
                'in_three_month': in_three_month,
                'in_six_month': in_six_month,
                'in_one_year': in_one_year,
                'befor_year': befor_year,
            },
            'amount': {
                'in_one_month': in_one_month_amount,
                'in_three_month': in_three_month_amount,
                'in_six_month': in_six_month_amount,
                'in_one_year': in_one_year_amount,
                'befor_year': befor_year_amount,
            }
        }, status=status.HTTP_200_OK)


class ManageTicketsCategory(viewsets.ModelViewSet):
    queryset = TicketCategory.objects.all()
    serializer_class = ManageAdminTicketCategorySerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data, partial=True)
        if ser.is_valid():
            ticket_cat = ser.validated_data.get("type", None)
            if not ticket_cat:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=ser.errors)
            TicketCategory.objects.create(type=ser.validated_data.get("type", None))
            return Response(data={'result': 'successfully created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        ticket_cat = self.get_object()
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ticket_cat.type = ser.validated_data['type']
            ticket_cat.save()
            return Response(data={'result': "successfully updated"}, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response(data={'result': 'successfully deleted'}, status=status.HTTP_200_OK)
