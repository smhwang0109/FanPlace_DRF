from django.core import serializers as django_serializers

from rest_framework import serializers
from accounts.serializers import UserSerializer
from actors.serializers import ActorSerializer
from .models import Article, ArticleComment, ArticleLike

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    actor = ActorSerializer(required=False)

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_comments(self, obj):
        return django_serializers.serialize('json', obj.comments.all(), ensure_ascii=False)

class ArticleCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    article = ArticleSerializer(required=False)
    class Meta:
        model = ArticleComment
        fields = '__all__'

