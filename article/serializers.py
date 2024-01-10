from rest_framework import serializers
from .models import Article
from user_management.serializers import CustomUserModelSerializer


class ArticleModelSerializer(serializers.ModelSerializer):
    author = CustomUserModelSerializer()  # Use your CustomUserSerializer here

    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['title', 'content']
