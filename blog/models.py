from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    created_at=models.DateTimeField(auto_now_add=True)
    
    # def total_likes(self):
    #     return self.likes.count()
    # class Meta:
    #     verbose_name = "Post"       
    #     verbose_name_plural = "Post"
    # def __str__(self):
    #     return self.title
    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def dislike_count(self):
        return self.dislikes.count()
    
class Like(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','post','session_key') 
        verbose_name = "Like"
        verbose_name_plural = "Like" 
    def __str__(self):
        return f"Like by {self.user or self.session_key} on {self.post.title}"


class Dislike(models.Model):
    user = models.ForeignKey(User,null=True, blank=True,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    post = models.ForeignKey(Post,related_name='dislikes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','post','session_key')
        verbose_name = "Dislike"
        verbose_name_plural = "Dislike"
    def __str__(self):
        return f"Dislike by {self.user or self.session_key} on {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    session_key = models.CharField(max_length=40, null=True, blank=True)  
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        if self.user:
            return f"Comment by {self.user.username}"
        elif self.session_key:
            return f"Comment by anonymous (session {self.session_key[:6]})"
        else:
            return "Anonymous comment"
    def is_reply(self):
        return self.parent is not None
    
    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    session_key = models.CharField(max_length=40, null=True, blank=True)      
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = "Comment Like"
        verbose_name_plural = "Comment Likes"
    def __str__(self):
        if self.user:
            return f"like by {self.user.username}"
        elif self.session_key:
            return f"liked by anonymous (session {self.session_key[:6]})"
        else:
            return "Anonymous liked"        #{self.comment.id}
    
    
class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    session_key = models.CharField(max_length=40, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = "Comment Dislike"
        verbose_name_plural = "Comment Dislikes"
    def __str__(self):
        if self.user:
            return f"dislike by {self.user.username}"
        elif self.session_key:
            return f"disliked by anonymous (session {self.session_key[:6]})"
        else:
            return "Anonymous disliked"  

