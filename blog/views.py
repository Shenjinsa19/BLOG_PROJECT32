from rest_framework import generics, permissions
from .permissions import IsOwnerOrAdmin
from blog.models import Post,Like,Dislike
from .models import Category
from .serializers import PostSerializer
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = request.user
        Dislike.objects.filter(user=user, post=post).delete()
        like_obj, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like_obj.delete()
            return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Post liked."}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = request.user
        Like.objects.filter(user=user, post=post).delete()
        dislike_obj, created = Dislike.objects.get_or_create(user=user, post=post)
        if not created:
            dislike_obj.delete()
            return Response({"message": "Dislike removed."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Post disliked."}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_disliked_posts(request):
    disliked_posts = [dislike.post for dislike in Dislike.objects.filter(user=request.user)]
    serializer = PostSerializer(disliked_posts, many=True, context={'request': request})
    return Response(serializer.data)

class PostListCreateView(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
    def get_permissions(self):
        if self.request.method=='POST':
            return[permissions.IsAuthenticated()]
        return []

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_permissions(self):
        if self.request.method in ['PUT','DELETE']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return []
class RegisterView(APIView):
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
from .serializers import LoginSerializer
from .serializers import RegisterSerializer
from rest_framework.permissions import BasePermission
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.author == request.user or request.user.is_staff



from .serializers import UserSerializer,CategorySerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=400)
        return Response(serializer.errors, status=400)
class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )   
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=201)
        return Response(serializer.errors, status=400)
