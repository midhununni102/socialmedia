from django.shortcuts import render
from rest_framework .response import Response
from rest_framework import viewsets
from api.serializers import UserSerializer,PostSerializer
from api.models import Posts
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import generics
from django.contrib.auth.models import User


class UserView(viewsets.ViewSet):

    def create(self,request,*args,**kw):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class PostView(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    




    def get_queryset(self):
        return Posts.objects.all().exclude(user=self.request.user)

    
   
    @action(methods=["POST"],detail=True)
    def add_post_like(self,request,*args, **kwargs):
        object=self.get_object()
        object.like.add(request.user)
        return Response(data="Post liked")

class PostPublishView(generics.UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        post.is_published = True
        post.save()
        return self.partial_update(request, *args, **kwargs)


class PostUnpublishView(generics.UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        post.is_published = False
        post.save()
        return self.partial_update(request, *args, **kwargs)