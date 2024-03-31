from django.db.models import F
from user_management.models import CustomUser
from django.http import Http404
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
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
from .permissions import IsAuthorOrReadOnly, CanDeleteArticle
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin


class CreateArticleView(View):
    template_name = 'user_management/create_article_page.html'

    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        context = {
            'BASE_API_URL': settings.BASE_API_URL,
            'form': form
        }
        return render(request, self.template_name, context)


class UpdateArticleView(View):
    template_name = 'user_management/update_article.html'
    # Apply the same permissions as in the APIView
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):

        context = {
            'BASE_API_URL': settings.BASE_API_URL,
        }
        return render(request, self.template_name, context)


# class CreateArticleView(View):
#     def get(self, request, *args, **kwargs):
#         # print('-------------------Article--------Get----')
#         form = ArticleForm()
#         return render(request, 'user_management/post.html', {'form': form})


class ArticleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        # print(f"-------article-------{serializer.data}")
        return Response(serializer.data)


class ArticlesAPIView(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ArticleModelSerializer

    def get_queryset(self):
        # Get the currently authenticated user
        user = self.request.user

        # Assuming "Author" is the name of the group
        author_group = Group.objects.get(name='Author')

        # Filter articles where the author is in the "Author" group
        queryset = Article.objects.filter(
            author__groups=author_group).order_by(F('created_at').desc())

        return queryset


class CreateArticleAPIView(generics.CreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        user = self.request.user

        # Check if the user has the 'add_article' permission through their group
        if user.has_perm('article.add_article'):
            print("---------------------got permission to add article")
            serializer.save(author=user)
        else:
            # Handle the case where the user doesn't have the required permission
            # You might want to raise a PermissionDenied exception or return an error response
            # For simplicity, let's raise a PermissionDenied exception here
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You do not have permission to add an article.")


class CheckPermisson(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        # Check object-level permissions
        token = get_token_from_request(request)
        if not token:
            return Response({'message': "Request doesn't contain token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({'message': 'Token not found'}, status=status.HTTP_401_UNAUTHORIZED)
        print(f"--------------{token.user}")
        print(f"----------------{article.author}")
        if token.user != article.author:
            return Response({'message': 'Permission denied'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': 'Permission granted'}, status=status.HTTP_200_OK)


class UpdateArticleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Article.objects.all()

    def put(self, request, article_id):
        print(f"articleid==========================={article_id}")
        article = get_object_or_404(Article, id=article_id)
        # Check object-level permissions
        self.check_object_permissions(self.request, article)

        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UpdateArticleAPIView(generics.UpdateAPIView):
#     print(f"---------------------------Update Article API===============================")

#     queryset = Article.objects.all()
#     serializer_class = ArticleModelSerializer


class DeleteArticleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanDeleteArticle]

    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"error": "Article does not exist"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, article)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BanAuthorAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, author_id):
        # Check if the user has the 'article.ban_author' permission
        user_to_ban = CustomUser.objects.get(id=author_id)

        if not request.user.has_perm('article.ban_author') or user_to_ban == request.user:
            print("-----------not have ban permission")
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        try:
            author_group = Group.objects.get(name='Author')

            user_to_ban.groups.remove(author_group)

            return Response({"detail": "User removed from 'Author' group"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            raise Http404("User not found")
        except Group.DoesNotExist:
            raise Http404("Group 'Author' not found")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
