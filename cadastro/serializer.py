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

    def create(self, validated_data):

        soma = Produto.objects.get(id=validated_data['produto'].id).preco * validated_data['quantidade']      
        carrinho = Carrinho.objects.get(cliente=validated_data['carrinho'].cliente)

        if (validated_data['quantidade'] > Produto.objects.get(id=validated_data['produto'].id).estoque):
            raise serializers.ValidationError("Quantidade maior do pedido excede quantidade do estoque")


        item = ItemCarrinho(
            carrinho = carrinho,
            produto = validated_data['produto'],
            quantidade = validated_data['quantidade'],
            subtotal = soma
        )
        item.save()

        carrinho.total += item.subtotal
        carrinho.save()


        return item

    def update(self, validated_data, instance):
        instance.quantidade = validated_data.get('quantidade', instance.quantidade)
        instance.save()
        
        return instance
    
    def delete(self, validated_data):
        carrinho = Carrinho.objects.get(cliente=validated_data['carrinho'].cliente)
        carrinho.total -= validated_data['subtotal']
        carrinho.save()

        item = ItemCarrinho.objects.get(id=validated_data['id'])
        item.delete()

        return item
