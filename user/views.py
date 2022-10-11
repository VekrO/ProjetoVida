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
        cnpj = request.POST.get('CNPJ')
        telefone = request.POST.get('telefone')
        password = request.POST.get('password')

        if(len(str(nome)) == 0 or len(str(email)) == 0 or len(str(password)) == 0):
            messages.error(request, 'Preencha todos os dados corretamente!')
            return redirect('registro')
        
        user = User()

        try:
            if(User.objects.filter(email=email).first()):
                messages.warning(request, 'E-mail já está em uso.')
                if(User.objects.filter(telefone=telefone).first()):
                    messages.warning(request, 'O telefone já está em uso.')
                    if(User.objects.filter(cnpj=cnpj).first()):
                        messages.warning(request, 'O CNPJ já está em uso.')
            else:
                user.nome = nome
                user.email = email
                user.cnpj = cnpj
                user.telefone = telefone
                user.set_password(password)
                user.save()

                # Executa o login.
                messages.success(request, 'Conta registrada com sucesso, faça login!')
                return redirect('login')
            return redirect('registro')

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

        # Verificar se a conta tem logo.
        user = User.objects.get(pk=request.user.pk)
        if(user.logo):
            if(user.logo.name == 'fotos/default.jpg'):
                # Adicionar uma mensagem para que o usuário possa atualizar a imagem dele.
                return render(request, 'src/painel.html', {'message': 'Você está usando a imagem padrão de logo, coloque outra!'})

        # Receber dados.
        dados = User.objects.get(pk=request.user.pk)
        return render(request, 'src/painel.html', {'dado': dados})
    
    def post(self, request):
        
        # Instânciar o usuário.
        user = User.objects.get(pk=request.user.pk)
        if(request.POST.get('trocar_logo') == 'sim'):
            
            # Alterar apenas a LOGO.
            if(len(request.FILES) != 0):
                
                # Salva a Logo Nova.
                logo = request.FILES.get('logo')
                
                # Remover antiga logo
                if(os.remove('{}{}'.format(BASE_DIR, user.logo.url))):
                    user.logo = logo
                else:
                    user.logo = logo
                user.save()
        else:

            if(user.nome == request.POST.get('nome')):
                messages.warning(request, 'Você não modificou o nome.')
                return redirect('painel')

            if(user.email == request.POST.get('email')):
                messages.warning(request, 'Você não modificiou o e-mail.')
                return redirect('painel')

            if(user.cnpj == request.POST.get('CNPJ')):
                messages.warning(request, 'Você não modificou o CNPJ.')
                return redirect('painel')

            if(user.telefone == request.POST.get('telefone')):
                messages.warning(request, 'Você não modificou o Telefone.')
                return redirect('painel')

            if(len(request.POST.get('descricao')) == 0):
                messages.warning(request, 'A descrição não pode ser vazia.')
                return redirect('painel')
            
            # Caso correto.
            user.nome = request.POST.get('nome')
            user.email = request.POST.get('email')
            user.telefone = request.POST.get('telefone')
            user.cnpj = request.POST.get('CNPJ')
            user.descricao = request.POST.get('descricao')
            user.save()

            messages.success(request, 'Conta atualizada com sucesso!')
        
        return redirect('painel')

# Conta update
class ContaUpdate(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['nome', 'email', 'cpf', 'cnpj', 'telefone']
    template_name = 'src/account-update.html'
    success_url = reverse_lazy('painel')

    def form_valid(self, form):

        # Remover imagem.
        user = User.objects.get(pk=self.request.user.pk)
        user.is_org = True

        # Verificar se a imagem já existe no banco de dados.
        if(os.path.exists('{}{}'.format(BASE_DIR, user.logo.url))):
            # Removo a imagem que já existe e crio uma nova.
            os.remove('{}{}'.format(BASE_DIR, user.logo.url))
        else:
            if(os.path.exists('{}{}'.format(BASE_DIR, user.logo.url))):
                print('Já está sendo usada. ')
        
        messages.success(self.request, 'Conta atualizada com sucesso!')
        return super().form_valid(form)