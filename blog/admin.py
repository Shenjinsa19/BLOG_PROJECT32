from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post,Category,Like,Dislike,Comment,CommentLike,CommentDislike

admin.site.register(Post)
# admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(CommentDislike)