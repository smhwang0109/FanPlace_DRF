from django.shortcuts import render, get_object_or_404
from .models import User, Follow
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class MyAccountView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        serializer_data = serializer.data
        followers = []
        for follower in user.followers.all():
            followers.append(follower.id)
        serializer_data['isMe'] = True
        serializer_data['isFollow'] = False
        serializer_data['followers'] = followers
        serializer_data['followers_cnt'] = user.followers.count()
        serializer_data['followings_cnt'] = user.followings.count()
        return Response(serializer_data)


class UserDetailView(APIView):
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        if user == request.user:
            isMe = True
        else:
            isMe = False
        if request.user.followings.filter(pk=user_pk).exists():
            isFollow = True
        else:
            isFollow = False

        serializer = UserSerializer(user)
        serializer_data = serializer.data
        followers = []
        for follower in user.followers.all():
            followers.append(follower.id)
        serializer_data['isMe'] = isMe
        serializer_data['isFollow'] = isFollow
        serializer_data['followers'] = followers
        serializer_data['followers_cnt'] = user.followers.count()
        serializer_data['followings_cnt'] = user.followings.count()
        return Response(serializer_data)


class UserFollowView(APIView):
    def post(self, request, to_user_pk):
        from_user = request.user
        to_user = get_object_or_404(User, pk=to_user_pk)
        if to_user.followers.filter(pk=from_user.pk).exists():
            follow = get_object_or_404(Follow, from_user=from_user, to_user=to_user)
            follow.delete()
        else:
            follow = Follow()
            follow.from_user = from_user
            follow.to_user = to_user
            follow.save()
        return Response()


class UserSearchView(APIView):
    def get(self, request, keyword):
        searched_users = User.objects.filter(username__icontains=keyword)
        serializer = UserSerializer(searched_users, many=True)
        return Response(serializer.data)
