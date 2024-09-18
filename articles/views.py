from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HeadArticle, SubHeadArticle, MiddleArticle, LastArticle
from .serializers import HeadArticleSerializer, SubHeadArticleSerializer, MiddleArticleSerializer, LastArticleSerializer


class HeadArticleView(APIView):
    serializer_class = HeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = HeadArticle.objects.all()
        ser_data = self.serializer_class(serializer, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class SubHeadArticleView(APIView):
    serializer_class = SubHeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        head_article_id = self.request.query_params.get('head_article', None)
        article_type = self.request.query_params.get('article_type', None)
        if article_type is None and head_article_id is None:
            return 1
        elif not article_type and head_article_id:
            return SubHeadArticle.objects.filter(head_article_id=head_article_id)
        sub_head_article = SubHeadArticle.objects.filter(head_article_id=head_article_id, type=article_type)
        return sub_head_article

    def get(self, request):
        query = self.get_queryset()
        if query == 1:
            return Response({'Bad Usage': 'insert type and head_article'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MiddleOrLastArticleView(APIView):
    serializer_class = MiddleArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sub_head_article_id = self.request.query_params.get('sub_head_article', None)
        middle_article_id = self.request.query_params.get('middle_article', None)
        if middle_article_id is None:
            pass
        else:
            return LastArticle.objects.filter(middle_article_id=middle_article_id).first()
        if sub_head_article_id is None:
            return 1
        if middle_article := MiddleArticle.objects.filter(sub_head_article_id=sub_head_article_id):
            return middle_article
        else:
            return LastArticle.objects.filter(sub_head_article_id=sub_head_article_id).first()

    def get(self, request):
        query = self.get_queryset()
        if query == 1:
            return Response({'Bad Usage': 'insert sub_head_article'}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(query, LastArticle):
            try:
                is_free = query.sub_head_article.is_free
            except:
                is_free = query.middle_article.sub_head_article.is_free

            if is_free:
                serializer = LastArticleSerializer(query, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif not is_free:
                if not request.user.is_pay:
                    return Response({'error': 'Payment required to access this resource.'}, status=403)
                serializer = LastArticleSerializer(query, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        middle_article = query.first()

        if isinstance(middle_article, MiddleArticle) and middle_article.sub_head_article.is_free:
            serializer = self.serializer_class(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif isinstance(middle_article, MiddleArticle) and not middle_article.sub_head_article.is_free:
            if not request.user.is_pay:
                return Response({'error': 'Payment required to access this resource.'}, status=403)
            serializer = self.serializer_class(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'some error occurred'}, status=status.HTTP_400_BAD_REQUEST)
