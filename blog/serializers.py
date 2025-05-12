from rest_framework import serializers
from blog.models import Post,Category,Like,Dislike,Comment,CommentLike
from django.contrib.auth.models import User
from blog.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']
        

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category', 'created_at', 'like_count', 'dislike_count', 'liked_by','comments']
    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()
    def get_dislike_count(self, obj):
        return Dislike.objects.filter(post=obj).count()
    def get_liked_by(self, obj):
        liked_users = []
        for like in obj.likes.all():
            if like.user:
                liked_users.append(like.user.username)
            elif like.session_key:
                liked_users.append(f"Anonymous ({like.session_key[:6]})")
        return liked_users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','author']

class LoginSerializer(serializers.ModelSerializer):
        username = serializers.CharField()
        password=serializers.CharField(write_only=True)
        class Meta:
             model=User
             fields=("username","password")
        def create(self,validated_data):
             user=User.objects.create_user(**validated_data)
             return()
             
class RegisterSerializer(serializers.ModelSerializer):
        username=serializers.CharField()
        email=serializers.CharField()
        password=serializers.CharField()
        class Meta:
            model=User
            fields=("username","email","password")
        def create(self,validated_data):
            user=User.objects.create_user(**validated_data)
            return()
                                                
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'username', 'content', 'parent', 'created_at', 'replies', 'like_count', 'liked_by']
        read_only_fields = ['id', 'user', 'session_key', 'post', 'created_at']
        extra_kwargs = {
            'user': {'required': False, 'allow_null': True},
            'session_key': {'required': False, 'allow_null': True},
        }
    
    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj).order_by('created_at')
        return CommentSerializer(replies, many=True, context=self.context).data

    def get_like_count(self, obj):
        return CommentLike.objects.filter(comment=obj).count()

    def get_liked_by(self, obj):
        return [like.user.username if like.user else f"Anonymous ({like.session_key[:6]})" for like in obj.likes.all()]

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        elif obj.session_key:
            return f"anon_{obj.session_key[:6]}"
        return "anonymous"
