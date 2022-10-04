from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('orgs/', views.ONGs.as_view(), name='ongs'),
]