from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( PostListCreateView, PostDetailView, UserListView,RegisterView,LoginView,CategoryListCreateView,like_post,dislike_post,my_disliked_posts,CommentListCreateView,CommentLikeView, CommentDetailWithRepliesView,CommentDislikeView)


urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  #crt post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  #post view
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('category/', CategoryListCreateView.as_view(), name='category-list'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),          #like a post
    path('posts/<int:post_id>/dislike/', dislike_post, name='dislike-post'),   #dislike a post
    path('posts/disliked/', my_disliked_posts, name='my-disliked-posts'),     #see what i disliked
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),#comm pnu
    path('comments/<int:comment_id>/like/', CommentLikeView.as_view(), name='comment-like'),#cmt like
    path('comments/<int:comment_id>/dislike/', CommentDislikeView.as_view(), name='comment-dislike'),  # Dislike comment
    path('comments/<int:pk>/', CommentDetailWithRepliesView.as_view(), name='comment-detail-with-replies')#cmt ku vanta response

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
