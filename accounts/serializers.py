from django.core import serializers as django_serializers

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    like_actors = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_articles(self, obj):
        return django_serializers.serialize('json', obj.articles.order_by('-created_at'), ensure_ascii=False)

    def get_like_actors(self, obj):
        return django_serializers.serialize('json', obj.like_actors.order_by('-popularity'), ensure_ascii=False)