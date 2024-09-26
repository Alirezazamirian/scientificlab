from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    # path('users/', views.ManageUsers.as_view(), name='ManageUsers'),
]

router = routers.DefaultRouter()
router.register(r'users', views.ManageUsers)
urlpatterns += router.urls
