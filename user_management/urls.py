from django.urls import path
from . import views

urlpatterns = [

    path('', views.LoginView.as_view(),
         name='login_page'),
    path('signup_page/', views.SignupView.as_view(),
         name='signup_page'),
    path('OTP_page/', views.OTPView.as_view(),
         name='OTP_page'),

    path('home_page/', views.HomeView.as_view(),
         name='home_page'),
    path('user_profile_page/', views.UserProfileView.as_view(),
         name='user_profile_page'),


    path('signup_API/', views.SignupAPIView.as_view(),
         name='signup_API'),
    path('user_account_API/', views.UserAccountView.as_view(),
         name='user_account_API'),
    path('get_auth_token_API/', views.CreateTokenAPIView.as_view(),
         name='get_auth_token_API'),
    path('user/', views.UserView.as_view(),
         name='user'),

]
