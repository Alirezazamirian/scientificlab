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



class LastArticleView(APIView):
    serializer_class = LastArticleSerializer
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, slug):
        if has_middle := self.get_queryset(slug).middle_article:
            if has_middle.sub_head_article.is_free:
                pass
            elif not has_middle.sub_head_article.is_free:
                if request.user.is_pay:
                    pass
                else:
                    return Response({'error': 'you are not able to see this doc'}, status=status.HTTP_403_FORBIDDEN)

        if has_sub := self.get_queryset(slug).sub_head_article:
            if has_sub.is_free:
                pass
            elif not has_sub.is_free:
                if request.user.is_pay:
                    pass
                else:
                    return Response({'error': 'you are not able to see this doc'}, status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self, slug):
        return LastArticle.objects.get(slug=slug)

    def get(self, request, slug):
        return self.get_last_article(slug)

    def get_last_article(self, slug):
        query = self.get_queryset(slug)
        if not query:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(query, partial=True)
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
            if dispatch_response := last_article_view.dispatch(request, slug):
                return dispatch_response
            return last_article_view.get_last_article(slug)
