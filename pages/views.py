from django.shortcuts import render

# Class Based Views
from django.views.generic.base import View
from user.models import User


# Tela Inicial
class Index(View):

    def get(self, request):
        ongs = User.objects.all()
        return render(request, 'src/index.html', {'ongs': ongs, 'ong_count': ongs.count()})


            

