from django.urls import path
from . import views

urlpatterns = [
    path('', views.HeadArticleView.as_view(), name='HeadArticleView'),
    path('test/<slug:slug>/', views.SubHeadArticleTestView.as_view(), name='SubHeadArticleView'),
    path('experminet/<slug:slug>/', views.SubHeadArticleExperimentView.as_view(), name='SubHeadArticleView'),
    path('middle-last/<slug:slug>/', views.MiddleArticleView.as_view(), name='MiddleArticleView'),
]
