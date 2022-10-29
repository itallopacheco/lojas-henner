from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (Categoria
, Cliente
, Endereco
, UnidadeFederativa
, Municipio
, Cartao
, Produto
, ProdutoImagens
, Carrinho
, ItemCarrinho
, Pedido)

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','primeiro_nome', 'ultimo_nome', 'data_nascimento', 'cpf', 'email', 'cartao', 'telefone','password']
    
    # def validate_password(self, value: str) -> str:
    #     return make_password(value)

    def create(self, validated_data):
        
        cliente = Cliente(
            primeiro_nome = validated_data['primeiro_nome'],
            ultimo_nome = validated_data['ultimo_nome'],
            data_nascimento = validated_data['data_nascimento'],
            cpf = validated_data['cpf'],
            email = validated_data['email'],
            telefone = validated_data['telefone'],
        )
        cliente.set_password(validated_data['password'])
        cliente.save()

        Carrinho.objects.create(cliente=cliente)

        return cliente

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

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nome']

class ProdutoImagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoImagens
        fields = ['produto', 'imagens']

    produto = ProdutoSerializer()

class CarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrinho
        fields = ['id', 'cliente', 'total']

class ItemCarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrinho
        fields = ['id', 'carrinho', 'produto', 'quantidade', 'subtotal']

    def update(self, validated_data, instance):
        instance.quantidade = validated_data.get('quantidade', instance.quantidade)
        instance.save()
        
        return instance
    
