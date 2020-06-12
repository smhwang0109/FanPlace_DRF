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
    class Meta:
        model = Review
        fields = '__all__'

class ReviewCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    review = ReviewSerializer(required=False)
    class Meta:
        model = ReviewComment
        fields = '__all__'
