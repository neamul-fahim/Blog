from rest_framework.authtoken.models import Token
from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Article
from .serializers import ArticleModelSerializer, ArticleSerializer
from rest_framework.authentication import TokenAuthentication
from django.views import View
from .forms import ArticleForm
from django.views.generic import TemplateView
from user_management.utility import get_token_from_request
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CreateArticleView(View):
    template_name = 'user_management/post.html'

    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, self.template_name, {'form': form})


class UpdateArticleView(View):
    template_name = 'user_management/update_article.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


# class CreateArticleView(View):
#     def get(self, request, *args, **kwargs):
#         # print('-------------------Article--------Get----')
#         form = ArticleForm()
#         return render(request, 'user_management/post.html', {'form': form})

class ArticleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        print(f"-------article-------{serializer.data}")
        return Response(serializer.data)


class ArticlesAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Article.objects.all()
    print(f"{queryset}")
    serializer_class = ArticleModelSerializer


class CreateArticleAPIView(generics.CreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdateArticleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, article_id):
        print(f"articleid==========================={article_id}")
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UpdateArticleAPIView(generics.UpdateAPIView):
#     print(f"---------------------------Update Article API===============================")

#     queryset = Article.objects.all()
#     serializer_class = ArticleModelSerializer


class DeleteArticleAPIView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    print(f"---------------------------Delete Article API===============================")

    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
