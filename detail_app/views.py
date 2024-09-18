from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContactUsSerializer, FavouriteSerializer
from .models import ContactUs, Favorite
from django.shortcuts import get_object_or_404


class ContactUsView(APIView):
    serializer_class = ContactUsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(self.request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'message was successfully sent'}, status=status.HTTP_200_OK)
        return Response({'error': 'data is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class FavouriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['GET', 'DELETE']

    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user).first()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            ser = self.serializer_class(queryset, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'there is no favourite list!'}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        query_params = self.request.query_params.getlist('article', None)
        queryset = self.get_queryset()
        selected_articles = queryset.articles
        for article in query_params:
            selected_articles.remove(article)
        queryset.save()
        return Response({'message': 'your favourite list was updated successfully'})
