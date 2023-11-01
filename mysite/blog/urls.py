from django.urls import path
from . import views

app_name = 'blog'
# {% url 'tube:post_list' %} 
# {% url 'tube:post_detail' post.pk %} 가능

urlpatterns = [
    path('<str:user_name>/', views.post_list, name='post_list'),
    path('<str:user_name>/new/', views.post_new, name='post_new'),
    path('<str:user_name>/<int:pk>/', views.post_detail, name='post_detail'),
    path('<str:user_name>/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<str:user_name>/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<str:user_name>/<int:pk>/comment/new/', views.comment_new, name='comment_new'),
    path('<str:user_name>/<int:pk>/comment/<int:cpk>/delete/', views.comment_delete, name='comment_delete'),
]