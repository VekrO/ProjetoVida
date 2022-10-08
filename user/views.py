import os
from django.shortcuts import redirect, render

# Class Based Views
from django.views.generic.base import View
from pages.models import Ongs 

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


# Evoluir Conta
class ContaEvoluir(View):

    def get(self, request):

        if(Ongs.objects.filter(nome_responsavel=request.user).exists()):
            messages.warning(request, 'Você não tem permissão para acessar, você já é uma ORG!')
            return redirect('painel')
        else:
            return render(request, 'src/conta-evoluir.html')

    def post(self, request):

        ong = Ongs()
        if len(request.FILES) != 0:
            ong.logo = request.FILES.get('logo')
        
        try:
            ong.nome_responsavel = request.user
            ong.cpf_responsavel = request.POST.get('cpf')
            ong.nome = request.POST.get('nome')
            ong.descricao = request.POST.get('descricao')
            ong.cnpj = request.POST.get('CNPJ')
            ong.email = request.POST.get('email')
            ong.save()

            # Adicioanar usuário como ORG.
            User.objects.update(is_org=True)

            messages.success(request, 'Sua conta agora é profissional.')
            return redirect('painel')

        except Exception as e:
            return render(request, 'src/conta-evoluir.html', {
            'nome': request.POST.get('nome'), 
            'email': request.POST.get('email'), 
            'cpf_responsavel': request.POST.get('cpf'),
            'descricao': request.POST.get('descricao'),
            'cnpj': request.POST.get('CNPJ'),
            'logo': request.FILES.get('logo')
        })

# Update Conta
class ContaUpdate(View):

    def get(self, request):
        ong = Ongs.objects.get(nome_responsavel=request.user)
        context = {
            'nome': ong.nome,
            'email': ong.email,
            'cpf_responsavel': ong.cpf_responsavel,
            'descricao': ong.descricao,
            'cnpj': ong.cnpj,
            'logo': ong.logo
        }
        return render(request, 'src/conta-update.html', context)
    
    def post(self, request):

        # Substituir imagem antiga.
        ong = Ongs.objects.get(nome_responsavel=request.user)
        ong.logo = request.FILES.get('logo')
        ong.save()
        
        try:
            Ongs.objects.filter(nome_responsavel=request.user).update(
                cpf_responsavel=request.POST.get('cpf'), 
                nome=request.POST.get('nome'),
                descricao=request.POST.get('descricao'),
                cnpj=request.POST.get('CNPJ'),
                email=request.POST.get('email'),
            )
            messages.success(request, 'Conta profissional atualizada com sucesso!')
            return redirect('painel')
        except Exception as e:
            print(e)
            messages.warning(request, 'Houve um erro ao tentar fazer atualização de dados.')
            return redirect('conta-update')

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

class Painel(View):

    def get(self, request):
        return render(request, 'src/painel.html')
