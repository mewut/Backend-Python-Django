from django.urls import path
from django.contrib import admin
from .views import News, PostDetail, PostCreate, PostUpdate, PostDelete, PostCreateArticle, PostUpdateArticle, ProfileUserUpdate

urlpatterns = [
    path('', News.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('add/', PostCreate.as_view(), name='create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('article/create/', PostCreateArticle.as_view(), name='post_create_article'),
    path('article/<int:pk>/edit/', PostUpdateArticle.as_view(), name='post_update_article'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_article'),
    path('profile/<int:pk>/update/', ProfileUserUpdate.as_view(), name='profile_user_update')

]
