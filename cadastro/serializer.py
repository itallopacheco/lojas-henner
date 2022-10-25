from rest_framework import serializers
from .models import Cliente, Endereco, UnidadeFederativa, Municipio, Cartao

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','primeiro_nome', 'ultimo_nome', 'data_nascimento', 'cpf', 'email', 'endereco', 'cartao','password']

class EnderecosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['id','rua','numero','bairro','cidade','estado','cep']

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