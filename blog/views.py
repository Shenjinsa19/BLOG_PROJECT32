from rest_framework import generics, permissions
from .permissions import IsOwnerOrAdmin
from blog.models import Post,Like,Dislike,Comment,CommentLike,CommentDislike
from .models import Category
from .serializers import PostSerializer,CommentSerializer,UserSerializer,CategorySerializer,RegisterSerializer,LoginSerializer
from django.shortcuts import render,redirect
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.permissions import IsAuthenticated,BasePermission
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,ListAPIView,RetrieveAPIView

class LikePostView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user.is_authenticated:
            like = Like.objects.filter(user=request.user, post=post).first()
            if like:
                like.delete()
                return Response({"message": "Like removed"})
            Dislike.objects.filter(user=request.user, post=post).delete()
            Like.objects.create(user=request.user, post=post)
            return Response({"message": "Post liked"})
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            like = Like.objects.filter(session_key=session_key, post=post).first()
            if like:
                like.delete()
                return Response({"message": "Like removed"})
            Dislike.objects.filter(session_key=session_key, post=post).delete()
            Like.objects.create(session_key=session_key, post=post)
            return Response({"message": "Post liked anonymously"})

        
class DislikePostView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if request.user.is_authenticated:
            dislike = Dislike.objects.filter(user=request.user, post=post).first()
            if dislike:
                dislike.delete()
                return Response({"message": "Dislike removed"})
            Like.objects.filter(user=request.user, post=post).delete()
            Dislike.objects.create(user=request.user, post=post)
            return Response({"message": "Post disliked"})
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            dislike = Dislike.objects.filter(session_key=session_key, post=post).first()
            if dislike:
                dislike.delete()
                return Response({"message": "Dislike removed"})
            Like.objects.filter(session_key=session_key, post=post).delete()
            Dislike.objects.create(session_key=session_key, post=post)
            return Response({"message": "Post disliked anonymously"})
  

class MyDislikedPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(dislike__user=self.request.user).distinct()



# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     def get_permissions(self):
#         if self.request.method in ['PUT','DELETE']:
#             return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
#         return []
    
# class RegisterView(APIView):
#     def post(self, request):
#         username=request.data.get('username')
#         email=request.data.get('email')
#         password=request.data.get('password')
#         if not username or not email or not password:
#             return Response({'error':'All fields are required.'}, status=400)
#         if User.objects.filter(username=username).exists():
#             return Response({'error':'username already exists.'},status=400)
#         user = User.objects.create_user(username=username,email=email,password=password)
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key}, status=201)
    
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.author == request.user or request.user.is_staff


# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]  

# class CategoryListCreateView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

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
    
class CommentLikeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user.is_authenticated:
            user = request.user
            like, created = CommentLike.objects.get_or_create(user=user, comment=comment)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            like, created = CommentLike.objects.get_or_create(session_key=session_key, comment=comment)
        if not created:
            like.delete()
            return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
        return Response({"message": "Comment liked."}, status=status.HTTP_201_CREATED)


class CommentDislikeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user.is_authenticated:
            user = request.user
            dislike, created = CommentLike.objects.get_or_create(user=user, comment=comment)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            dislike, created = CommentLike.objects.get_or_create(session_key=session_key, comment=comment)

        if not created:
            dislike.delete()
            return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
        return Response({"message": "Comment disliked."}, status=status.HTTP_201_CREATED)

    
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post,id=post_id)
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user, post=post)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            session_key = self.request.session.session_key
            serializer.save(user=None, session_key=session_key, post=post)
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent=None).order_by('-created_at')
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Comment
from .serializers import CommentSerializer

class CommentReplyView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(parent_id=comment_id).order_by('created_at')

    def perform_create(self, serializer):
      parent_comment = Comment.objects.get(id=self.kwargs['comment_id'])
      serializer.save(parent=parent_comment, post=parent_comment.post)


# class CommentReplyView(generics.ListAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]
#     def get_queryset(self):
#         comment_id = self.kwargs['comment_id']
#         return Comment.objects.filter(parent_id=comment_id).order_by('created_at')

class CommentDetailWithRepliesView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('post_list_create_view') 
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test
def admin_login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/admin/')
        else:
            error = "Invalid admin credentials"
    return render(request, 'blog/admin_login.html', {'error': error})

from django.contrib.auth.decorators import login_required
from .forms import PostForm
@login_required
def post_list_create_view(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect('post_list_create_view')
    else:
        form = PostForm()

    return render(request, 'blog/post_list_create_view.html', {'posts': posts, 'form': form})

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'blog/user_list_view.html', {'users': users})

# @login_required
# def post_detail_view(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    like_count = post.likes.count()
    dislike_count = post.dislikes.count()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'like_count': like_count,
        'dislike_count': dislike_count,
    })

@login_required
def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list_view.html', {'categories': categories})

# def comment_list_create_view(request):

