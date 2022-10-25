from multiprocessing.connection import Client
from django.http import JsonResponse
from cadastro.serializer import ClientesSerializer, EnderecosSerializer, UnidadesFederativasSerializer, MunicipiosSerializer, ListaEnderecoClienteSerializer
from rest_framework import viewsets, generics
from cadastro.models import Cliente, Endereco, UnidadeFederativa, Municipio, Cartao
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

class ClientesViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [AllowAny]
        
        

class EnderecosViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Enderecos"""
    permission_classes = (IsAuthenticated,)
    queryset = Endereco.objects.all()
    serializer_class = EnderecosSerializer


class ListaEnderecoClienteViewSet(generics.ListAPIView):
    """ Exibindo todos os Enderecos de um cliente"""
    def get_queryset(self):
        id_endereco = Cliente.objects.get(pk=self.kwargs['pk']).endereco
        queryset = Endereco.objects.filter(pk=id_endereco.pk)
        return queryset
    serializer_class = ListaEnderecoClienteSerializer