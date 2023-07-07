from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='posts_lst'),
<<<<<<< HEAD
    path('<int:pk>/', PostDetail.as_view(), name='post_dtl'),
    path('search/', PostSearch.as_view(), name='post_searching'),
    path('create/', PostCreate.as_view(), name='post_creation'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
=======
    path('<int:id>/', PostDetail.as_view(), name='post_dtl'),
]
>>>>>>> 38b278149551e42a18b4f44b3dcd7ac5364e08b9
