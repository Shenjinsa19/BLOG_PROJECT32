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
                                                

