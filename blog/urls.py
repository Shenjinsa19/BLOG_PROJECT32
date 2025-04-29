from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views  
from .views import createview,detailview,UserListView

urlpatterns = [
    path('create/', createview.as_view(), name='create'),
    path('detail/<int:pk>/', detailview.as_view(), name='detail'),
    path('register/', views.register.as_view(), name='register'),
    path('login/', views.login.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
