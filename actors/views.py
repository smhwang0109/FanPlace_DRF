from django.shortcuts import render, get_object_or_404
from django.conf import settings

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

class ActorListView(APIView):
    # ActorList
    def get(self, request):
        actors = Actor.objects.filter(like_users=request.user)
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    # ActorCreate
    def post(self, request):
        actorId = request.data['actorId']
        data = requests.get(f'https://api.themoviedb.org/3/person/{actorId}?api_key={API_KEY}&language=ko-KR').json()
        
        null = ''

        if data['place_of_birth'].split()[-1] == 'Korea':
            for s in data['also_known_as']:
                if isHangul(s):
                    name = s
                    break
            else:
                name = data['name']
        else:
            name = data['name']
        
        actor_data = {
            'id': data['id'],
            'name': name,
            'birthday': data['birthday'],
            'deathday': data['deathday'],
            'gender': data['gender'],
            'profile_path': data['profile_path'],
            'popularity': data['popularity']
        }
        serializer = ActorSerializer(data=actor_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            movie_create(actorId)
            return Response(serializer.data)
        return Response(serializer.errors)

class ActorDetailView(APIView):
    def get_actor(self, actor_pk):
        return get_object_or_404(Actor, pk=actor_pk)
    
    # ActorDetail
    def get(self, request, actor_pk):
        actor = self.get_actor(actor_pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data)
   
class ActorLikeView(APIView):
    def get_actor(self, actor_pk):
        return get_object_or_404(Actor, pk=actor_pk)

    # Like
    def post(self, request, actor_pk):
        actor = self.get_actor(actor_pk)
        if actor.like_users.filter(pk=request.user.id).exists():
            actorlike = get_object_or_404(ActorLike, user=request.user, actor=actor)
            actorlike.delete()
        else:
            actorlike = ActorLike()
            actorlike.user = request.user
            actorlike.actor = actor
            actorlike.save()
        return Response()

