from django.core import serializers as django_serializers

from rest_framework import serializers
from accounts.serializers import UserSerializer
from actors.serializers import ActorSerializer
from .models import Article, ArticleComment, ArticleLike

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.http import JsonResponse

class MyJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return dict(obj)
        return super().default(obj)

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    actor = ActorSerializer(required=False)

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_comments(self, obj):
        # return list(obj.comments.all())
        return django_serializers.serialize('json', obj.comments.all(), cls=MyJSONEncoder, ensure_ascii=False)
        # return json.dumps(list(obj.comments.all().values()), )

class ArticleCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    article = ArticleSerializer(required=False)
    class Meta:
        model = ArticleComment
        fields = '__all__'

