from django.urls import path
from . import views

urlpatterns = [
    path('user/registro/', views.Registro.as_view(), name='Registro')
]
