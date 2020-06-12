from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Movie, Review, ReviewComment
from .serializers import MovieSerializer, ReviewSerializer, ReviewCommentSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class MovieListView(APIView):
    model = Movie
    
    # MovieList(피드)
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
        
    # MovieCreate
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class ReviewListView(APIView):
    def get_movie(self, movie_pk):
        return get_object_or_404(Movie, pk=movie_pk)

    # ReviewList
    def get(self, request, movie_pk):
        movie = self.get_movie(movie_pk)
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    # ReviewCreate
    def post(self, request, movie_pk):
        movie = self.get_movie(movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data)

class ReviewDetailView(APIView):
    def get_review(self, review_pk):
        return get_object_or_404(Review, pk=review_pk)
    
    # ReviewUpdate
    def put(self, request, movie_pk, review_pk):
        review = self.get_review(review_pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # ReviewDelete
    def delete(self, request, movie_pk, review_pk):
        review = self.get_review(review_pk)
        review.delete()
        return Response()
            
class ReviewCommentListView(APIView):
    def get_review(self, review_pk):
        return get_object_or_404(Review, pk=review_pk)

    # ReviewCommentList
    def get(self, request, movie_pk, review_pk):
        review = self.get_review(self, review_pk)
        comments = review.comments.all()
        serializer = ReviewCommentSerializer(review, many=True)
        return Response(serializer.data)

    # ReviewCommentCreate
    def post(self, request, movie_pk, review_pk):
        review = self.get_review(self, review_pk)
        serializer = ReviewCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data)

class ReviewCommentDetailView(APIView):
    def get_comment(self, comment_pk):
        return get_object_or_404(ReviewComment, pk=comment_pk)
    
    # ReviewCommentUpdate
    def put(self, request, movie_pk, review_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        serializer = ReviewCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # ReviewCommentDelete
    def delete(self, request, movie_pk, review_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        comment.delete()
        return Response()
