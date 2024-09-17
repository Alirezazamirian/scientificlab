from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HeadArticle, SubHeadArticle, MiddleArticle, LastArticle
from .serializers import HeadArticleSerializer, SubHeadArticleSerializer, MiddleArticleSerializer


class HeadArticleView(APIView):
    serializer_class = HeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = HeadArticle.objects.all()
        ser_data = self.serializer_class(serializer, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class FreeSubHeadArticleView(APIView):
    serializer_class = SubHeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        head_article_id = self.request.query_params.get('head_article', None)
        article_type = self.request.query_params.get('article_type', None)
        if not article_type:
            return SubHeadArticle.objects.filter(head_article_id=head_article_id, is_free=True)
        if not article_type and not head_article_id:
            return Response({'Bad Usage':'insert type and head_article'}, status=status.HTTP_400_BAD_REQUEST)
        sub_head_article = SubHeadArticle.objects.filter(head_article_id=head_article_id, type=article_type, is_free=True)
        return sub_head_article

    def get(self, request):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseSubHeadArticleView(APIView):
    serializer_class = SubHeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        head_article_id = self.request.query_params.get('head_article', None)
        article_type = self.request.query_params.get('article_type', None)
        if not article_type:
            return SubHeadArticle.objects.filter(head_article_id=head_article_id)
        if not article_type and not head_article_id:
            return Response({'Bad Usage':'insert type and head_article'}, status=status.HTTP_400_BAD_REQUEST)
        sub_head_article = SubHeadArticle.objects.filter(head_article_id=head_article_id, type=article_type)
        return sub_head_article

    def get(self, request):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        if self.request.user.is_pay:
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'error':'access denied, you must purchase first'}, status=status.HTTP_400_BAD_REQUEST)


class MiddleArticleView(APIView):
    serializer_class = MiddleArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sub_head_article_id = self.request.query_params.get('sub_head_article', None)
        if middle_article := MiddleArticle.objects.filter(sub_head_article_id=sub_head_article_id):
            return middle_article
        else:
            return LastArticle.objects.filter(sub_head_article_id=sub_head_article_id)


    def get(self, request):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)