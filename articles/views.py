from django.shortcuts import render, get_object_or_404

from .models import Article, ArticleComment, ArticleLike
from .serializers import ArticleSerializer, ArticleCommentSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ArticleListView(APIView):
    # ArticleList
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # ArticleCreate
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
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

    # CommentList
    def get(self, request, article_pk):
        article = self.get_article(article_pk)
        comments = article.comments.all()
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data)

    # CommentCreate
    def post(self, request, article_pk):
        article = self.get_article(article_pk)
        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
        return Response(serializer.data)

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
    def get(self, request, article_pk):
        article = self.get_article(article_pk)
        if article.like_users.filter(pk=request.user.id).exists():
            # article.like_users.remove(request.user)
            articlelike = get_object_or_404(ArticleLike, user=request.user, article=article)
            articlelike.delete()
        else:
            # article.like_users.add(request.user)
            articlelike = ArticleLike()
            articlelike.user = request.user
            articlelike.article = article
            articlelike.save()
        return Response()

