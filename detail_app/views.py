from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContactUsSerializer, FavouriteSerializer, ScoreSerializer, BlogSerializer, BlogCategorySerializer
from .models import ContactUs, Favorite, Star, BlogCategory, Blog


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
        if Star.objects.filter(user=self.request.user):
            return Response({'error': 'each user can score once!'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer == 1:
            return Response({'error': 'score must be 1 to 5!'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            Star.objects.create(user=self.request.user, article_id=params, score=serializer.validated_data['score'])
            return Response({'message': 'score was added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogView(APIView):
    serializer_class = BlogCategorySerializer

    def get_queryset(self):
        return BlogCategory.objects.all()

    def get(self, request):
        cat_blogs = self.get_queryset()
        serializer = self.serializer_class(cat_blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)