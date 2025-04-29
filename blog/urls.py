from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( PostListCreateView, PostDetailView, UserListView,RegisterView,LoginView,CategoryListCreateView)


urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('category/', CategoryListCreateView.as_view(), name='category-list'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
