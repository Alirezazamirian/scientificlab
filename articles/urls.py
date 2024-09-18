from django.urls import path
from . import views

urlpatterns = [
    path('head-article/', views.HeadArticleView.as_view(), name='HeadArticleView'),
    path('free-sub-head-article/', views.SubHeadArticleView.as_view(), name='FreeSubHeadArticleView'),
    path('middle-or-last-article/', views.MiddleOrLastArticleView.as_view(), name='MiddleOrLastArticleView'),
]
