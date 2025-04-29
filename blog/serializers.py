from rest_framework import serializers
from .models import myusers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = myusers
        fields = ['id','title','content','author','created_at']
        read_only_fields = ['author','created_at']
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

