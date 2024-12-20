from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('contact-us/', views.ContactUsView.as_view(), name='ContactUsView'),
    path('score/', views.ScoreView.as_view(), name='ScoreView'),
    path('blog/', views.BlogCategoryView.as_view(), name='BlogView'),
    path('tickets/', views.TicketView.as_view(), name='TicketView'),
    path('tickets-category/', views.TicketCategoryView.as_view(), name='TicketCategoryView'),
    path('user-count/', views.UserCountView.as_view(), name='UserCountView'),
]


router = routers.SimpleRouter()
router.register(r'favourite', views.FavouriteView)
urlpatterns += router.urls
