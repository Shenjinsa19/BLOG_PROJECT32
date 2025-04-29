from django.db import models
from django.contrib.auth.models import User
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
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Post"       
        verbose_name_plural = "Post"
    def __str__(self):
        return self.title

