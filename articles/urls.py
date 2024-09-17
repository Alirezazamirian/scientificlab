from django.urls import path, include
from . import views

urlpatterns = [
    path('head-article/', views.HeadArticleView.as_view(), name='HeadArticleView'),
    path('free-sub-head-article/', views.FreeSubHeadArticleView.as_view(), name='FreeSubHeadArticleView'),
    path('purchase-sub-head-article/', views.PurchaseSubHeadArticleView.as_view(), name='PurchaseSubHeadArticleView'),
]
