from django.urls import path
from . import views

urlpatterns = [
    path('check_permission/<int:article_id>/', views.CheckPermisson.as_view(),
         name='check_permission'),
    path('post_article_page/', views.CreateArticleView.as_view(),
         name='post_article_page'),
    path('update_article_page/', views.UpdateArticleView.as_view(),
         name='update_article_page'),
    path('get_article/<int:article_id>/',
         views.ArticleAPIView.as_view(), name='get_article'),
    path('all_articles/', views.ArticlesAPIView.as_view(),
         name='all_articles'),
    path('update_article/<int:article_id>/',
         views.UpdateArticleAPIView.as_view(), name='update_article'),
    path('delete_article/<int:pk>/',
         views.DeleteArticleAPIView.as_view(), name='delete_article'),
    path('post_article_API/', views.CreateArticleAPIView.as_view(),
         name='post_article_API'),
    path('ban_author_API/<int:author_id>/', views.BanAuthorAPIView.as_view(),
         name='ban_author_API'),
]
