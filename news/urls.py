from django.urls import path
from django.contrib import admin
from .views import News, PostDetail, PostCreate, PostUpdate, PostDelete, ProfileUserUpdate, add_subscribe, del_subscribe, IndexView, SearchList

urlpatterns = [
    path('', News.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('add/', PostCreate.as_view(), name='create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('profile/<int:pk>/update/', ProfileUserUpdate.as_view(), name='profile_user_update'),
    path('<int:pk>/add_subscribe', add_subscribe),
    path('<int:pk>/del_subscribe', del_subscribe),
    path('<int:pk>/search', SearchList.as_view(), name='search'),
    path('', IndexView.as_view()),
]
