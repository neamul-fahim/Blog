from django.urls import path
from . import views

urlpatterns = [
    path('get_user/', views.UserProfileAPIView.as_view(), name='get_user'),
    path('get_all_users/', views.AllUserProfileAPIView.as_view(),
         name='get_all_users'),
    path('login_page/', views.LoginView.as_view(),
         name='login_page'),
    path('signup_page/', views.SignupView.as_view(),
         name='signup_page'),
    path('OTP_page/', views.OTPView.as_view(),
         name='OTP_page'),

    path('', views.HomeView.as_view(),
         name='home_page'),
    path('user_profile_page/', views.UserProfileView.as_view(),
         name='user_profile_page'),


    path('signup_API/', views.SignupAPIView.as_view(),
         name='signup_API'),
    path('user_account_API/', views.UserAccountView.as_view(),
         name='user_account_API'),
    path('get_auth_token_API/', views.CreateTokenAPIView.as_view(),
         name='get_auth_token_API'),
    path('blocked_users_page/', views.BlockedUsersPage.as_view(),
         name="blocked_users_page"),
    path('blocked_users/', views.BlockedUsersAPIView.as_view(), name="blocked_users"),
    path('unblock_user/<int:user_id>/',
         views.UnblockUserAPIView.as_view(), name='unblock_user'),
    path('moderator_users_page/', views.ModeratorUsersPage.as_view(),
         name='moderator_users_page'),
    path('toggle_moderator/<int:user_id>/',
         views.ToggleModeratorAPIView.as_view(), name='toggle_moderator'),


    #     path('user/', views.UserView.as_view(),
    #          name='user'),

]
