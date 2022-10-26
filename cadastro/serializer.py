from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Categoria, Cliente, Endereco, UnidadeFederativa, Municipio, Cartao, Produto, ProdutoImagens, Categoria

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','primeiro_nome', 'ultimo_nome', 'data_nascimento', 'cpf', 'email', 'cartao', 'telefone','password']
    def validate_password(self, value: str) -> str:
        return make_password(value)

class EnderecosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['id','rua','numero','bairro','cidade','estado','cep', 'cliente']

class UnidadesFederativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeFederativa
        fields = '__all__'

class MunicipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

class ListaEnderecoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['id','rua','numero','bairro','cidade','estado','cep']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nome']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'thumbnail', 'marca', 'categoria']

        categoria = CategoriaSerializer()


class ProdutoImagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoImagens
        fields = ['produto', 'imagens']

    produto = ProdutoSerializer()