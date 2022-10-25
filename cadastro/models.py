from django.db import models
from cpf_field.models import CPFField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date


class ClienteManager(BaseUserManager):

    def create_user(self, cpf, primeiro_nome, ultimo_nome, email, data_nascimento, password=None):
        if not email:
            raise ValueError('O usuário deve ter um email')
        if not cpf:
            raise ValueError('O usuário deve ter um CPF')
        if not primeiro_nome:
            raise ValueError('O usuário deve ter um nome')
        user = self.model(
            cpf=cpf,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            email=self.normalize_email(email),
            data_nascimento = data_nascimento,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, primeiro_nome, ultimo_nome, email, data_nascimento, password=None):
        user = self.create_user(
            cpf=cpf,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            email=self.normalize_email(email),
            data_nascimento = data_nascimento,
            
            
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UnidadeFederativa(models.Model):
    codigo = models.CharField(max_length=2, primary_key=True)
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return u'%s/%s' % (self.nome, self.sigla)


class Municipio(models.Model):
    estado = models.ForeignKey(UnidadeFederativa, related_name="municipios", on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6, unique=True)
    nome = models.CharField(max_length=60)

    def __str__(self):
        return "%s/%s" % (self.nome, self.estado.sigla)



class Cartao(models.Model):
    numero = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    validade = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.numero + ' ' + self.nome + ' ' + self.validade + ' ' + self.codigo

class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cidade = models.ForeignKey(Municipio, on_delete=models.CASCADE, default = '', verbose_name='Cidade')
    estado = models.ForeignKey(UnidadeFederativa, on_delete=models.CASCADE, default = '', verbose_name='Estado')
    cep = models.CharField(max_length=100)

    def __str__(self):
        return self.rua + ' ' + str(self.numero) + ' ' + self.bairro + ' ' + str(self.cidade) + ' ' + str(self.estado) + ' ' + self.cep


class Cliente(AbstractBaseUser):
    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = CPFField(max_length=11, unique=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, default = '',null =True, blank=True , verbose_name='Endereço')
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, default = '',null =True ,blank=True ,verbose_name='Cartão')

    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ClienteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primeiro_nome', 'ultimo_nome', 'cpf', 'data_nascimento']

    def __str__(self):
        return self.primeiro_nome + ' ' + self.ultimo_nome

    def has_perms(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    @property
    def idade(self):
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

