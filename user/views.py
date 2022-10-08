from django.shortcuts import redirect, render, HttpResponse

# Class Based Views
from django.views.generic.base import View
from pages.models import Ongs 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

# Messages
from django.contrib import messages

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



        #ong = Ongs()

        #ong.nome_responsavel = request.user
        #ong.cpf_responsavel = request.POST.get('cpf_responsavel')

        #ong.nome = request.POST.get('nome_ong')
        #ong.descricao = request.POST.get('descricao_ong')
        #ong.cnpj = request.POST.get('cnpj_ong')
        #ong.email = request.POST.get('email_ong')
        #ong.password = request.POST.get('senha_ong')

        #if len(request.FILES) != 0:
        #    ong.logo = request.FILES.get('logo_ong')
        
        #ong.save()

        return redirect('index')

# Tela de Login
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