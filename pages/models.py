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
    logo = models.ImageField(upload_to="fotos/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    

