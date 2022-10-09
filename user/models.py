from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Controlador de usuários.
class UserManager(BaseUserManager):
    def create_user(self, nome, email, password=None):

        if not email:
            raise ValueError('Insira o e-mail corretamente.')
        user = self.model(
            nome=nome,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nome, email, password):

        user = self.create_user(
            nome=nome,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

# Tabela de usuários
class User(AbstractBaseUser):

    nome = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=255,
        unique=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Configurações de ONG.
    is_org = models.BooleanField(default=False)
    cpf = models.CharField(max_length=14, null=True, blank=False, verbose_name="CPF")
    cnpj = models.CharField(max_length=14, null=True, blank=False, verbose_name="CNPJ")
    telefone = models.CharField(max_length=13, null=True, blank=False, verbose_name="Telefone")
    logo = models.ImageField(upload_to='fotos/', null=True, blank=False, verbose_name="Imagem")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome',]
    
    objects = UserManager()

    def __str__(self):
        return self.nome
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    