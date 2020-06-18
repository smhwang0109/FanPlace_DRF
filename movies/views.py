from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.conf import settings

from actors.models import Actor
from .models import Movie, Genre, MovieGenre, MovieActor, Review, ReviewComment 
from .serializers import MovieSerializer, ReviewSerializer, ReviewCommentSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import requests
import random

API_KEY_LIST = [settings.THEMOVIEDB_API_KEY_SOOM, settings.THEMOVIEDB_API_KEY_SUN]
API_KEY = random.choice(API_KEY_LIST)

# MovieCreate & ConnectActor(Actor 생성 이후에 실행될 함수)
def movie_create(actorId):
    data = requests.get(f'https://api.themoviedb.org/3/person/{actorId}/movie_credits?api_key={API_KEY}&language=ko-KR').json()
    null = False
    for movie in data['cast']: # 영화별로 순회하면서
        # if not movie['poster_path']:
        #     continue
        if not Movie.objects.filter(id=movie['id']):
            # 1. 영화 기본정보 저장
            movie_data = dict()
            for attr in ['id', 'original_title', 'overview', 'poster_path', 'release_date', 'popularity']:
                try:
                    movie_data[attr] = movie[attr]
                except:
                    pass
            serializer = MovieSerializer(data=movie_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response(serializer.errors)

            # 2. 영화-장르 관계 저장
            for genre_id in movie['genre_ids']:
                movie_for_genre = get_object_or_404(Movie, pk=movie_data['id'])
                genre_for_movie = get_object_or_404(Genre, pk=genre_id)
                moviegenre = MovieGenre()
                moviegenre.movie = movie_for_genre
                moviegenre.genre = genre_for_movie
                moviegenre.save()

        # 3. 영화-배우 관계 저장
        movie_for_actor = get_object_or_404(Movie, pk=movie['id'])
        actor_for_movie = get_object_or_404(Actor, pk=actorId)
        movieactor = MovieActor()
        movieactor.movie = movie_for_actor
        movieactor.actor = actor_for_movie
        movieactor.character = movie['character']
        movieactor.save()

    return Response()

# 영화 검색을 통해 해당 영화 리뷰 작성할 경우 시
def movie_create_one(movieId):
    null = False
    data = requests.get(f'https://api.themoviedb.org/3/movie/{movieId}?api_key={API_KEY}&language=ko-KR').json()
    # if not data['poster_path']:
    #     return Response()
    if not Movie.objects.filter(id=movieId):
        movie_data = dict()
        for attr in ['id', 'original_title', 'overview', 'poster_path', 'release_date', 'popularity']:
            try:
                movie_data[attr] = movie[attr]
            except:
                pass
        serializer = MovieSerializer(data=movie_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors)

        # 2. 영화-장르 관계 저장
        for genre in data['genres']:
            movie_for_genre = get_object_or_404(Movie, pk=movie_data['id'])
            genre_for_movie = get_object_or_404(Genre, pk=genre['id'])
            moviegenre = MovieGenre()
            moviegenre.movie = movie_for_genre
            moviegenre.genre = genre_for_movie
            moviegenre.save()

    return Response()

##################################
# Movie

class MovieListView(APIView):
    # MovieList(피드)
    def get(self, request):
        like_actors = Actor.objects.filter(like_users=request.user)
        movies = Movie.objects.none()
        for actor in like_actors:
            movies = movies.union(Movie.objects.filter(actors=actor))
        serializer = MovieSerializer(movies.order_by('-popularity'), many=True)
        return Response(serializer.data)

class ActorMovieListView(APIView):
    # 출연작
    def get(self, request, actorId):
        actor = get_object_or_404(Actor, id=actorId)
        movies = actor.movies.all()
        serializer = MovieSerializer(movies.order_by('-popularity'), many=True)
        return Response(serializer.data)

##################################
# Review

class ReviewListView(APIView):
    def get_movie(self, movie_pk):
        return get_object_or_404(Movie, pk=movie_pk)

    # ReviewList
    def get(self, request, movie_pk):
        movie = self.get_movie(movie_pk)
        reviews = movie.reviews.order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    # ReviewCreate
    def post(self, request, movie_pk):
        # 만약 해당 영화가 우리 DB에 없다면 => DB에 저장
        if not Movie.objects.filter(pk=movie_pk):
            movie_create_one(movie_pk)

        movie = self.get_movie(movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data)
        return Response(serializer.errors)

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
        return Response(serializer.errors)

    # ReviewDelete
    def delete(self, request, movie_pk, review_pk):
        review = self.get_review(review_pk)
        review.delete()
        return Response()

##################################
# ReviewComment

class ReviewCommentListView(APIView):
    def get_review(self, review_pk):
        return get_object_or_404(Review, pk=review_pk)

    # ReviewCommentList
    def get(self, request, movie_pk, review_pk):
        review = self.get_review(review_pk)
        comments = review.comments.all()
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data)

    # ReviewCommentCreate
    def post(self, request, movie_pk, review_pk):
        review = self.get_review(review_pk)
        request.data['username'] = request.user.username
        serializer = ReviewCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data)
        return Response(serializer.errors)

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
        return Response(serializer.errors)

    # ReviewCommentDelete
    def delete(self, request, movie_pk, review_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        comment.delete()
        return Response()