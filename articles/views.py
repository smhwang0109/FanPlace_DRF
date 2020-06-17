#-*- coding:utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from actors.models import Actor
from .models import Article, ArticleComment, ArticleLike
from .serializers import ArticleSerializer, ArticleCommentSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ArticleListView(APIView):
    # ArticleList (피드)
    def get(self, request):
        like_actors = Actor.objects.filter(like_users=request.user)
        articles = Article.objects.none()
        for following in request.user.followings.all():
            articles = articles.union(following.articles.all())
        for like_actor in like_actors:
            articles = articles.union(like_actor.articles.all())
        serializer = ArticleSerializer(articles.order_by('-created_at'), many=True)
        return Response(serializer.data)

    # ArticleCreate
    def post(self, request):
        actorId = request.data['actorId']
        actor = get_object_or_404(Actor, id=actorId)
        request.data['username'] = request.user.username
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, actor=actor)
            return Response(serializer.data)
        return Response(serializer.errors)

class ArticlePopularListView(APIView):
    # ArticlePopularList (인기)
    def get(self, request):
        articles = Article.objects.all()
        articles = sorted(articles, key=lambda article: article.popularity, reverse=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ActorArticleListView(APIView):
    # 배우 게시물
    def get(self, request, actorId):
        actor = get_object_or_404(Actor, id=actorId)
        articles = actor.articles.all()
        articles = sorted(articles, key=lambda article: article.popularity, reverse=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class UserArticleListView(APIView):
    # 유저 게시물
     def get(self, request, user_id):
        User = get_user_model()
        user = get_object_or_404(User, id=user_id)
        articles = user.articles.all()
        articles = sorted(articles, key=lambda article: article.popularity, reverse=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleDetailView(APIView):
    def get_article(self, article_pk):
        return get_object_or_404(Article, pk=article_pk)
    
    # ArticleDetail
    def get(self, request, article_pk):
        article = self.get_article(article_pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # ArticleUpdate
    def put(self, request, article_pk):
        article = self.get_article(article_pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # ArticleDelete
    def delete(self, request, article_pk):
        article = self.get_article(article_pk)
        article.delete()
        return Response()

class ArticleCommentListView(APIView):
    def get_article(self, article_pk):
        return get_object_or_404(Article, pk=article_pk)

    # CommentCreate
    def post(self, request, article_pk):
        article = self.get_article(article_pk)
        request.data['username'] = request.user.username
        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
        return Response(serializer.errors)

class ArticleCommentDetailView(APIView):
    def get_comment(self, comment_pk):
        return get_object_or_404(ArticleComment, pk=comment_pk)

    # CommentUpdate
    def put(self, request, article_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        serializer = ArticleCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # CommentDelete
    def delete(self, request, article_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        comment.delete()
        return Response()

class ArticleLikeView(APIView):
    def get_article(self, article_pk):
        return get_object_or_404(Article, pk=article_pk)

    # Like
    def post(self, request, article_pk):
        article = self.get_article(article_pk)
        if article.like_users.filter(pk=request.user.id).exists():
            articlelike = get_object_or_404(ArticleLike, user=request.user, article=article)
            articlelike.delete()
        else:
            articlelike = ArticleLike()
            articlelike.user = request.user
            articlelike.article = article
            articlelike.save()
        return Response()


class ArticleSearchView(APIView):
    def get(self, request, keyword):
        searched_articles = Article.objects.filter(content__icontains=keyword)
        actors = Actor.objects.filter(name__icontains=keyword)
        for actor in actors:
            searched_articles = searched_articles.union(actor.articles.all())
        searched_articles = sorted(searched_articles, key=lambda article: article.popularity, reverse=True)
        serializer = ArticleSerializer(searched_articles, many=True)
        return Response(serializer.data)