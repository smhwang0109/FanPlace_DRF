from django.core import serializers as django_serializers

from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Movie, Review, ReviewComment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    movie = MovieSerializer(required=False)
    
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_comments(self, obj):
        return django_serializers.serialize('json', obj.comments.order_by('-created_at'), ensure_ascii=False)

class ReviewCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    review = ReviewSerializer(required=False)
    class Meta:
        model = ReviewComment
        fields = '__all__'
