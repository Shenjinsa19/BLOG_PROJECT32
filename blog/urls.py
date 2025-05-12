from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( RegisterView,LoginView,CommentListCreateView,LikePostView,DislikePostView,MyDislikedPostsView,CommentLikeView, CommentDetailWithRepliesView,CommentDislikeView,register_view,login_view,admin_login_view,post_list_create_view,post_detail_view,user_list_view,category_list_view)


urlpatterns = [
    # path('posts/', PostListCreateView.as_view(), name='post-list-create'),  #crt post
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  #post view,edit,delete
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('users/', UserListView.as_view(), name='user-list'),
    # path('category/', CategoryListCreateView.as_view(), name='category-list'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),          #like a post
    path('posts/<int:post_id>/dislike/', DislikePostView.as_view(),name='dislike-post'),   #dislike a post
    path('posts/disliked/', MyDislikedPostsView.as_view(), name='my-disliked-posts'),     #see what i disliked
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(),name='post-comments'),#comm pnu
    path('comments/<int:comment_id>/like/', CommentLikeView.as_view(),name='comment-like'),#cmt like
    path('comments/<int:comment_id>/dislike/', CommentDislikeView.as_view(),name='comment-dislike'),  # Dislike comment
    path('comments/<int:pk>/', CommentDetailWithRepliesView.as_view(),name='comment-detail-with-replies'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('admin-login/', admin_login_view, name='admin-login'),#admin
    path('posts/', post_list_create_view, name='post_list_create_view'),#create aslo view
    path('users/', user_list_view, name='user-list-view'),#any user view
    path('posts/<int:pk>/', post_detail_view, name='post-detail-view'),  #post view,edit,delete
    path('category/', category_list_view, name='category-list')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
