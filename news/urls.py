from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='posts_lst'),
    path('<int:pk>/', PostDetail.as_view(), name='post_dtl'),
    path('search/', PostSearch.as_view(), name='post_searching'),
    path('create/', PostCreate.as_view(), name='post_creation'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:id>/', PostDetail.as_view(), name='post_dtl'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]

