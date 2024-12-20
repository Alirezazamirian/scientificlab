from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .serializers import (ContactUsSerializer, FavouriteSerializer, ScoreSerializer, BlogSerializer,
                          BlogCategorySerializer, TicketSerializer, TicketCategorySerializer)
from .models import ContactUs, Favorite, Star, BlogCategory, Blog, Ticket, TicketCategory


class ContactUsView(APIView):
    serializer_class = ContactUsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.POST)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response({'message': 'message was successfully sent'}, status=status.HTTP_200_OK)
        return Response({'error': 'data is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class FavouriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'delete',]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            ser = self.serializer_class(queryset, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'there is no favourite list!'}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        params = self.request.query_params.get('article_id', None)
        if params:
            Favorite.objects.create(user=request.user, articles_id=params)
            return Response({'message': 'favourite was created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'insert article_id'}, status=status.HTTP_400_BAD_REQUEST)


class ScoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def post(self, request):
        params = self.request.query_params.get('article_id', None)
        data = self.request.POST
        serializer = self.serializer_class(data=data)
        if Star.objects.filter(user=self.request.user, article_id=params):
            return Response({'error': 'each user can score once!'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer == 1:
            return Response({'error': 'score must be 1 to 5!'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            Star.objects.create(user=self.request.user, article_id=params, score=serializer.validated_data['score'])
            return Response({'message': 'score was added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogCategoryView(APIView):
    serializer_class = BlogCategorySerializer

    def get_queryset(self):
        return BlogCategory.objects.all()

    def get(self, request):
        cat_blogs = self.get_queryset()
        serializer = self.serializer_class(cat_blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(user=self.request.user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        parent_id = self.request.query_params.get('parent_id', None)
        cat = self.request.query_params.get('ticket_category', None)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            Ticket.objects.create(user=self.request.user,
                                  title=serializer.validated_data['title'],
                                  description=serializer.validated_data['description'],
                                  parent_id=parent_id,
                                  ticket_category=cat,
                                  is_appropriate=serializer.validated_data['is_appropriate'])
            return Response(data={'message': 'ticket was created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketCategorySerializer

    def get_queryset(self):
        return TicketCategory.objects.all()

    def get(self, request):
        cat_ticket = self.get_queryset()
        serializer = self.serializer_class(cat_ticket, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCountView(APIView):

    def get_queryset(self):
        return User.objects.all()

    def get(self, request):
        query = self.get_queryset()
        user_count = query.count()
        if user_count > 0:
            bachelor_count = 0
            master_count = 0
            phd_count = 0
            fellowship_count = 0
            for user in query:
                if user.degree == 'bachelor':
                    bachelor_count += 1
                if user.degree == 'master':
                    master_count += 1
                if user.degree == 'phd':
                    phd_count += 1
                if user.degree == 'fellowship':
                    fellowship_count += 1
            return Response({
                'user_count': user_count,
                'bachelor_count': bachelor_count,
                'master_count': master_count,
                'phd_count': phd_count,
                'fellowship_count': fellowship_count
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'some error occurred!'}, status=status.HTTP_400_BAD_REQUEST)
