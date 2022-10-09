import os
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy
import requests

# Class Based Views
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

# Messages
from django.contrib import messages
from projetovida.settings import BASE_DIR

# User Models
from user.models import User
from django.contrib.auth.forms import UserChangeForm

# Tela de Registro
class Registro(View):

    def get(self, request):

        if(request.user.is_authenticated):
            return redirect('index')

        return render(request, 'src/registro.html')

    def post(self, request):
        
        # Criar um cadastro para usuários.
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if(len(str(nome)) == 0 or len(str(email)) == 0 or len(str(password)) == 0):
            messages.error(request, 'Preencha todos os dados corretamente!')
            return redirect('registro')
        
        user = User()

        try:
            if(User.objects.filter(email=email).first()):
                messages.warning(request, 'E-mail já está em uso.')
                return redirect('registro')
            else:
                user.nome = nome
                user.email = email
                user.set_password(password)
                user.save()

                # Executa o login.
                return render(request, 'src/login.html', {'email': email, 'password':password})

        except Exception as e:
            messages.error(request, e)
            return redirect('registro')

# Tela de Logins
class Login(View):

    def get(self, request):
        # Não deixa o usuário fazer login, caso conectado!
        if(request.user.is_authenticated):
            return redirect('index')

        return render(request, 'src/login.html')
        
    def post(self, request):
        
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        # Verificar se o usuário existe.
        if(user):
            if(user.is_active):
                # Loga o usuário.
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Sua conta não está ativada!')
                return redirect('login')
        else:
            messages.error(request, 'Nenhum usuário encontrado, verifique os dados.')
            return redirect('login')
        
class Logout(View):

    # Executa o logout
    def get(self, request):
        logout(request)
        messages.error(request, "Você saiu, conecte-se novamente!")
        return redirect('login')

class Painel(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'src/painel.html')

# Conta update
class ContaUpdate(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['nome', 'email', 'cpf', 'cnpj', 'telefone', 'logo']
    template_name = 'src/account-update.html'
    success_url = reverse_lazy('painel')

    def form_valid(self, form):
        # Remover imagem.
        user = User.objects.get(pk=self.request.user.pk)
        old_image = user.logo.url
        user.is_org = True
        user.save()

        # Remove imagem antiga.
        os.remove('{}{}'.format(BASE_DIR, old_image))

        # Confirma
        messages.success(self.request, 'Conta atualizada com sucesso!')

        return super().form_valid(form)