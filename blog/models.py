from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
    def __str__(self):
        return self.name
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    created_at=models.DateTimeField(auto_now_add=True)
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = "Post"       
        verbose_name_plural = "Post"
    def __str__(self):
        return self.title
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','post') 
        verbose_name = "Like"
        verbose_name_plural = "Like" 
class Dislike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='dislikes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','post')
        verbose_name = "Dislike"
        verbose_name_plural = "Dislike"