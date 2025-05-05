from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( PostListCreateView, PostDetailView, UserListView,RegisterView,LoginView,CategoryListCreateView,like_post,dislike_post,my_disliked_posts)


urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('category/', CategoryListCreateView.as_view(), name='category-list'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
    path('posts/<int:post_id>/dislike/', dislike_post, name='dislike-post'),
    path('posts/disliked/', my_disliked_posts, name='my-disliked-posts')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
