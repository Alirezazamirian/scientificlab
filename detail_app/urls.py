from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('contact-us/', views.ContactUsView.as_view(), name='ContactUsView'),
]


router = routers.SimpleRouter()
router.register(r'favourite', views.FavouriteView)
urlpatterns += router.urls
