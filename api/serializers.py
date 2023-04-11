from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    like=serializers.CharField(read_only=True)
    post_like_count=serializers.CharField(read_only=True)

    class Meta:
        model=Posts
        fields="__all__"

