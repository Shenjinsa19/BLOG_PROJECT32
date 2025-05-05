from rest_framework import serializers
from blog.models import Post,Category,Like,Dislike
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']
from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category', 'created_at', 'like_count', 'dislike_count', 'liked_by' ]

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_dislike_count(self, obj):
        return Dislike.objects.filter(post=obj).count()

    def get_liked_by(self, obj):
        return [like.user.username for like in Like.objects.filter(post=obj)]


from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
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
                                                

