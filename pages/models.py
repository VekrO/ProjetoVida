from django.db import models
from user.models import User

class Postagem(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    imagem = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name="Imagem")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title