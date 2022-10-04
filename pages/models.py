from django.db import models
from user.models import User

class Ongs(models.Model):

    # Dados do Usuário
    nome_responsavel = models.ForeignKey(User, on_delete=models.PROTECT)
    cpf_responsavel = models.CharField(max_length=255)
    
    # Dados de uma ONGs
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    cnpj = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

