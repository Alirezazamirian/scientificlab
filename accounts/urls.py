from django.urls import path, include
from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='RegisterView'),
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('verification/', views.EmailVerificationView.as_view(), name='EmailVerificationView'),
    path('logout/', views.LogoutView.as_view(), name='LogoutView'),
    path('user/', views.AccountManagementView.as_view(), name='AccountManagementView'),
    path('forget-pass/', views.ForgetPassView.as_view(), name='ForgetPassView'),
    path('forget-pass-verification/', views.ForgetPassVerifyView.as_view(), name='ForgetPassVerifyView'),
]
