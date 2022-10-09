from django.shortcuts import render

# Class Based Views
from django.views.generic.base import View
from user.models import User


# Tela Inicial
class Index(View):

    def get(self, request):
        return render(request, 'src/index.html')

# Tela de Ongs
class ONGs(View):

    def get(self, request):
        ongs = User.objects.all()
        return render(request, 'src/orgs.html', {'ongs': ongs})
    


            

