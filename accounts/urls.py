from django.urls import path, include
from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='RegisterView'),
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('verification/', views.EmailVerificationView.as_view(), name='EmailVerificationView'),
]