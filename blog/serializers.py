from rest_framework import serializers
from .models import myusers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = myusers
        fields = ['id','title','content','author','created_at']
        read_only_fields = ['author','created_at']
