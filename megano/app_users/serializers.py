from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get("fullName")
        user = User.objects.get(id=instance.user.id)
        user.email = validated_data.get("user").get("email")
        user.save()
        instance.phone = validated_data.get("phone")
        instance.save()
        return instance
