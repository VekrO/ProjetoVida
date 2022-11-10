from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# Class Based Views
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, DeleteView
from user.models import User
from .models import Postagem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Tela Inicial
class Index(View):

    def get(self, request):
        ongs = User.objects.all()
        return render(request, 'src/index.html', {'ongs': ongs, 'ong_count': ongs.count()})

class Blog(View):

    def get(self, request):
        dados = Postagem.objects.all()
        return render(request, 'src/blog.html', {'dados': dados})

    def post(self, request):
        
        post = Postagem()
        post.user = request.user
        post.title = request.POST.get('title')
        post.description = request.POST.get('title')
        if(len(request.FILES) != 0):
            post.imagem = request.FILES.get('file')
            post.save()
        else:
            post.imagem = 'default.jpg'
            post.save()

        messages.success(request, 'Postagem adicionada com sucesso!')
        return redirect('blog')

class editBlog(LoginRequiredMixin, UpdateView):

    model = Postagem
    fields = ['title', 'description', 'imagem']
    template_name = 'src/form.html'
    success_url = reverse_lazy('blog')

class deleteBlog(LoginRequiredMixin, DeleteView):

    model = Postagem
    success_url = reverse_lazy('blog')
    template_name = 'src/formDelete.html' 

