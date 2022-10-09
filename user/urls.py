from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.Registro.as_view(), name='registro'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('painel/', views.Painel.as_view(), name='painel'),
    path('painel/conta/update/<int:pk>', views.ContaUpdate.as_view(), name='conta-update'),
]
