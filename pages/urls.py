from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('blog/', views.Blog.as_view(), name='blog'),
    path('blog/edit/<int:pk>/', views.editBlog.as_view(), name='editBlog'),
    path('blog/delete/<int:pk>/', views.deleteBlog.as_view(), name='deleteBlog'),
]