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


class SubHeadArticleTestView(APIView):
    serializer_class = SubHeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sub_head_article = SubHeadArticle.objects.filter(type='Test')
        return sub_head_article

    def get(self, request, slug):
        query = self.get_queryset().filter(slug=slug)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubHeadArticleExperimentView(APIView):
    serializer_class = SubHeadArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sub_head_article = SubHeadArticle.objects.filter(type='Experiment')
        return sub_head_article

    def get(self, request, slug):
        query = self.get_queryset().filter(slug=slug)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# class MiddleOrLastArticleView(APIView):
#     serializer_class = MiddleArticleSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         sub_head_article_id = self.request.query_params.get('sub_head_article', None)
#         middle_article_id = self.request.query_params.get('middle_article', None)
#         if middle_article_id is None:
#             pass
#         else:
#             return LastArticle.objects.filter(middle_article_id=middle_article_id).first()
#         if sub_head_article_id is None:
#             return 1
#         if middle_article := MiddleArticle.objects.filter(sub_head_article_id=sub_head_article_id):
#             return middle_article
#         else:
#             return LastArticle.objects.filter(sub_head_article_id=sub_head_article_id).first()
#
#     def get(self, request):
#         query = self.get_queryset()
#         if query == 1:
#             return Response({'Bad Usage': 'insert sub_head_article'}, status=status.HTTP_400_BAD_REQUEST)
#
#         if isinstance(query, LastArticle):
#             try:
#                 is_free = query.sub_head_article.is_free
#             except:
#                 is_free = query.middle_article.sub_head_article.is_free
#
#             if is_free:
#                 serializer = LastArticleSerializer(query, partial=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             elif not is_free:
#                 if not request.user.is_pay:
#                     return Response({'error': 'Payment required to access this resource.'}, status=403)
#                 serializer = LastArticleSerializer(query, partial=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#
#         middle_article = query.first()
#
#         if isinstance(middle_article, MiddleArticle) and middle_article.sub_head_article.is_free:
#             serializer = self.serializer_class(query, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif isinstance(middle_article, MiddleArticle) and not middle_article.sub_head_article.is_free:
#             if not request.user.is_pay:
#                 return Response({'error': 'Payment required to access this resource.'}, status=403)
#             serializer = self.serializer_class(query, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'some error occurred'}, status=status.HTTP_400_BAD_REQUEST)


class LastArticleView(APIView):
    serializer_class = LastArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LastArticle.objects.all()

    def get(self, request, slug):
        return self.get_last_article(slug)

    def get_last_article(self, slug):
        query = self.get_queryset().filter(slug=slug)
        if not query.exists():
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MiddleArticleView(APIView):
    serializer_class = MiddleArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        if MiddleArticle.objects.filter(slug=slug).exists():
            query = MiddleArticle.objects.filter(slug=slug)
            serializer = self.serializer_class(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            last_article_view = LastArticleView()
            return last_article_view.get_last_article(slug)
