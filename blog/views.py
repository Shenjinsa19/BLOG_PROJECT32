from rest_framework import generics, permissions
from .permissions import IsOwnerOrAdmin
from .models import myusers
from .serializers import PostSerializer
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class createview(generics.ListCreateAPIView):
    queryset=myusers.objects.all()
    serializer_class=PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method=='POST':
            return[permissions.IsAuthenticated()]
        return []

class detailview(generics.RetrieveUpdateDestroyAPIView):
    queryset=myusers.objects.all()
    serializer_class=PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_permissions(self):
        if self.request.method in ['PUT','DELETE']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return []
class register(APIView):
    def post(self, request):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        if not username or not email or not password:
            return Response({'error':'All fields are required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error':'username already exists.'},status=400)

        user = User.objects.create_user(username=username,email=email,password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=201)

class login(APIView):
    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)
        if user:
            token, created=Token.objects.get_or_create(user=user)
            return Response({'token':token.key})
        return Response({'error':'invalid details'}, status=400)

from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.author == request.user or request.user.is_staff



