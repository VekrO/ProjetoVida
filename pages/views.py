from django.shortcuts import render

# Class Based Views
from django.views.generic.base import View

# Tela Inicial
class Index(View):

    def get(self, request):
        return render(request, 'src/index.html')

# Tela de Registro
class ONGs(View):

    def get(self, request):
        return render(request, 'src/ongs.html')
