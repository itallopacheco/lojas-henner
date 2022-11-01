from email.policy import default
from enum import Enum
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
    cliente = models.ForeignKey('Cliente', related_name='cartoes', default='' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.numero + ' ' + self.nome + ' ' + self.validade + ' ' + self.codigo

class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.ForeignKey(Municipio, on_delete=models.CASCADE, default = '', verbose_name='Cidade')
    estado = models.ForeignKey(UnidadeFederativa, on_delete=models.CASCADE, default = '', verbose_name='Estado')
    cep = models.CharField(max_length=100)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, default = '', verbose_name='Cliente')

    def __str__(self):
        return self.rua + ' ' + str(self.numero) + ' ' + self.bairro + ' ' + str(self.cidade) + ' ' + str(self.estado) + ' ' + self.cep

class Cliente(AbstractBaseUser):
    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = CPFField(max_length=11, unique=True)

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

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    @property
    def idade(self):
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    preco = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default = '', verbose_name='Categoria')
    thumbnail = models.ImageField(upload_to='imagens/', default = '', verbose_name='Imagem')
    estoque = models.IntegerField()
    marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nome 

class ProdutoImagens(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default = '', verbose_name='Produto')
    imagens = models.FileField(upload_to='imagens/')

    def __str__(self):
        return self.produto.nome

class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, default = '', verbose_name='Cliente')
    total = models.FloatField(default=0)

    def __str__(self):
        return  'carrinho ' + ' de ' + self.cliente.primeiro_nome + ' ' + self.cliente.ultimo_nome
  
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, default = '', verbose_name='Carrinho')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default = '', verbose_name='Produto')
    quantidade = models.IntegerField()
    subtotal = models.FloatField(default=0)
    
    def __str__(self):
        return self.produto.nome + ' ' + str(self.quantidade)

PEDIDO_STATUS =(
    ('1', "Pendente"),
    ('2', "Aprovado"),
    ('3', "Cancelado"),
    ('4', "Entregue"),
)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default = '', verbose_name='Cliente')
    status = models.CharField(max_length=1, choices=PEDIDO_STATUS, default='1')
    data = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, default = '', verbose_name='Endereço')
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, default = '', verbose_name='Carrinho')
    total = models.FloatField(default=0)