from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from .models import Profile, Avatar, User
from .serializers import ProfileSerializer


class SignInView(APIView):
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        serialized_data = list(request.data.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    def post(self, request):
        user = request.user
        old_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")
        if not user.check_password(old_password):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


def updateAvatar(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        avatar = Avatar.objects.get_or_create(src=request.FILES["avatar"])[0]
        profile.avatar = avatar
        profile.save()
        return HttpResponse(status=status.HTTP_200_OK)
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
