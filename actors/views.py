from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse

from movies.views import movie_create
from .models import Actor, ActorLike
from .serializers import ActorSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import requests
import re
import random

API_KEY_LIST = [settings.THEMOVIEDB_API_KEY_SOOM, settings.THEMOVIEDB_API_KEY_SUN]
API_KEY = random.choice(API_KEY_LIST)

def isHangul(text):
    encText = text
    hanCount = len(re.findall(u"[\u3130-\u318F\uAC00-\uD7A3]+", encText))
    return hanCount > 0

def actor_create(actor_id):

    data = requests.get(f'https://api.themoviedb.org/3/person/{actor_id}?api_key={API_KEY}&language=ko-KR').json()
    
    null = ''

    for s in data['also_known_as']:
        if isHangul(s):
            name = s
            break
    else:
        name = data['name']
    
    actor_data = {}
    for attr in ['id', 'name', 'birthday', 'deathday', 'gender', 'profile_path', 'popularity']:
        try:
            actor_data[attr] = data[attr]
        except:
            pass
    serializer = ActorSerializer(data=actor_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        movie_create(actor_id)
        return Response(serializer.data)
    return Response(serializer.errors)

class ActorListView(APIView):
    def get(self, request):
        actors = Actor.objects.filter(like_users=request.user)
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

class ActorPopularListView(APIView):
    # ActorPopularList (인기)
    def get(self, request):
        actors = Actor.objects.all()
        actors = sorted(actors, key=lambda actor: actor.popularity, reverse=True)
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

class ActorDetailView(APIView):
    def get_actor(self, actor_pk):
        return get_object_or_404(Actor, pk=actor_pk)
    
    # ActorDetail
    def get(self, request, actor_pk):
        if not Actor.objects.all().filter(pk=actor_pk).exists():
            actor_create(actor_pk)
        actor = self.get_actor(actor_pk)
        serializer = ActorSerializer(actor)
        serializer_data = serializer.data
        if request.user in actor.like_users.all():
            is_like = True
        else:
            is_like = False
        serializer_data['is_like'] = is_like 
        return Response(serializer_data)
   
class ActorLikeView(APIView):
    def get_actor(self, actor_pk):
        return get_object_or_404(Actor, pk=actor_pk)

    # LikeData
    def get(self, request, actor_pk):
        actor = self.get_actor(actor_pk)
        if actor.like_users.filter(pk=request.user.id).exists():
            is_like = True
        else:
            is_like = False
        data = {
            'like_count': actor.like_users.count(),
            'is_like': is_like
        }
        return JsonResponse(data)

    # Like
    def post(self, request, actor_pk):
        actor = self.get_actor(actor_pk)
        if actor.like_users.filter(pk=request.user.id).exists():
            actorlike = get_object_or_404(ActorLike, user=request.user, actor=actor)
            actorlike.delete()
            is_like = False
        else:
            actorlike = ActorLike()
            actorlike.user = request.user
            actorlike.actor = actor
            actorlike.save()
            is_like = True
        data = {
            'like_count': actor.like_users.count(),
            'is_like': is_like
        }
        return JsonResponse(data)
