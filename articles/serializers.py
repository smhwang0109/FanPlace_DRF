from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Article, ArticleComment, ArticleLike

# class ArticleLikeSerializer(serializers.ModelSerializer):
#     # user = UserSerializer(required=False)
#     # article = ArticleSerializer(required=False)
#     class Meta:
#         model = ArticleLike
#         fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    # like_users = ArticleLikeSerializer(read_only=True, many=True)
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    article = ArticleSerializer(required=False)
    class Meta:
        model = ArticleComment
        fields = '__all__'

