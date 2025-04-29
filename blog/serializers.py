from rest_framework import serializers
from .models import Post,Category

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','content','author','category','author','created_at']
        read_only_fields = ['author','created_at']
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
