from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( CommentListCreateView,post_like_view,post_dislike_view,my_disliked_posts_view,comment_replies_view, comment_detail_with_replies_view,register_view,login_view,admin_login_view,post_list_create_view,post_detail_view,user_list_view,category_list_view,comment_like_view,comment_dislike_view,posts_by_category_view,PostDeleteView)


urlpatterns = [
    # path('posts/', PostListCreateView.as_view(), name='post-list-create'),  #crt post
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  #post view,edit,delete
    # path('register/', RegisterView.as_view(), name='register'),
    #path('login/', LoginView.as_view(), name='login'),
    # path('users/', UserListView.as_view(), name='user-list'),
    # path('category/', CategoryListCreateView.as_view(), name='category-list'),
   


    path('posts/<int:post_id>/like/', post_like_view, name='like-post'),          #like a post 
    path('posts/<int:post_id>/dislike/', post_dislike_view,name='dislike-post'),   #dislike a post 
    path('my_disliked_posts/', my_disliked_posts_view, name='my-disliked-posts'),     #see what i disliked
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(),name='comment-list-create'),#post ku comm pnu
    path('comments/<int:comment_id>/comments/', comment_replies_view,name='replies'),#anta cmmt ku nested cmt.......issues
    path('comments/<int:comment_id>/like/', comment_like_view,name='comment-like'),#cmt like
    path('comments/<int:comment_id>/dislike/', comment_dislike_view,name='comment-dislike'),  # Dislike comment
    path('comments/<int:pk>/', comment_detail_with_replies_view,name='comment-detail'),#replies of a specific cmt pk......pending
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),#delete here only auth admin



    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('admin-login/', admin_login_view, name='admin-login'),#admin
    path('posts/', post_list_create_view, name='post_list_create_view'),#create aslo view
    path('users/', user_list_view, name='user-list-view'),#any user view
    path('posts/<int:pk>/', post_detail_view, name='post-detail-view'),  #post view,like,dislike
    path('category/', category_list_view, name='category-list'),#view cater
    path('category/<int:category_id>/posts/', posts_by_category_view, name='posts-by-category')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
