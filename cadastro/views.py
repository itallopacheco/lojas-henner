from django_filters.rest_framework import DjangoFilterBackend
from multiprocessing.connection import Client
from django.http import JsonResponse
from rest_framework.decorators import action
from cadastro.serializer import *
from rest_framework import viewsets, generics, response
from cadastro.models import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated , AllowAny, IsAdminUser
from .permissions import IsOwner, IsOwnerAddress
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenViewBase,
)
from django.http import *
from rest_framework_simplejwt.serializers import(
    TokenObtainPairSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import filters


# Create your views here.

class ClientesViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()               

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Não foi possível encontrar uma conta com essas credenciais',
    
    }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def get_queryset(self):
        queryset = Cliente.objects.filter(id = self.request.user.id)
        return queryset

class CategoriaViewSet(viewsets.ModelViewSet):
    """ Exibindo todas as Categorias"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

class ProdutosViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Produtos"""
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria']
    search_fields = ['nome', 'marca']

class UnidadeFederativaViewSet(viewsets.ModelViewSet):
    """ Exibindo todas as Unidades Federativas"""
    queryset = UnidadeFederativa.objects.all()
    serializer_class = UnidadesFederativasSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

class MunicipioViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Municipios"""
    queryset = Municipio.objects.all()
    serializer_class = MunicipiosSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class EnderecosViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Enderecos"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Endereco.objects.all()
    serializer_class = EnderecosSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cliente = request.user)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data
            , status=status.HTTP_201_CREATED
            , headers=headers
            )

    def get_object(self):
       pk = self.kwargs.get('pk')
       obj = get_object_or_404(self.get_queryset(), pk=pk)

       self.check_object_permissions(self.request, obj)
       return obj
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsOwnerAddress(), ]
        return super().get_permissions()


class ListaEnderecoClienteViewSet(generics.ListAPIView):
    """ Exibindo todos os Enderecos de um cliente"""
    def get_queryset(self):
        id_endereco = Cliente.objects.get(pk=self.kwargs['pk']).endereco
        queryset = Endereco.objects.filter(pk=id_endereco.pk)
        return queryset
    serializer_class = ListaEnderecoClienteSerializer

class ItemCarrinhoViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Itens do Carrinho"""
    queryset = ItemCarrinho.objects.all()
    serializer_class = ItemCarrinhoSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        queryset = ItemCarrinho.objects.filter(carrinho__cliente=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        produto = Produto.objects.get(pk=request.data['produto'])
        soma = request.data['quantidade'] * produto.preco
        carrinho = request.user.carrinho
        
        if (request.data['quantidade'] > produto.estoque):
            return response.Response(
                {'Erro': 'Quantidade maior que o estoque'}
                , status=status.HTTP_400_BAD_REQUEST
                )
    
        serializer.save(carrinho = carrinho
                        ,subtotal = soma
                        )
        
        carrinho.total += soma
        carrinho.save() 

        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data
            , status=status.HTTP_201_CREATED
            , headers=headers
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            carrinho = Carrinho.objects.get(pk=instance.carrinho.pk)
            carrinho.total -= instance.subtotal
            carrinho.save()

            self.perform_destroy(instance)
        except Http404:
            pass
        return response.Response(status=status.HTTP_204_NO_CONTENT) 
   
    @action(detail=True, methods=['patch'])
    def destroy_all(self, request, *args, **kwargs):
        carrinho = Carrinho.objects.get(pk=request.user.carrinho.pk)
        carrinho.total = 0
        carrinho.save()
        self.get_queryset().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        itemCarrinho = ItemCarrinho.objects.get(pk=self.kwargs['pk'])
        produto = Produto.objects.get(pk=itemCarrinho.produto.pk)
        carrinho = Carrinho.objects.get(pk=request.user.carrinho.pk)


        if(request.data.get('quantidade') + itemCarrinho.quantidade > produto.estoque):
            return response.Response(
                {'Erro': 'Quantidade maior que o estoque'}
                , status=status.HTTP_400_BAD_REQUEST
                )
        

        print("AAAAAAAAAAAA", request.data.get('quantidade'))
        print("BBBBBBBBBBBB", itemCarrinho.quantidade)

        if (request.data.get('quantidade') > itemCarrinho.quantidade):
            soma = (request.data.get('quantidade')  * produto.preco) -  itemCarrinho.subtotal
            itemCarrinho.quantidade = request.data.get('quantidade')
            itemCarrinho.subtotal += soma
            itemCarrinho.save()
            carrinho.total += soma
            carrinho.save()
        else:
            subtracao =  itemCarrinho.subtotal - (request.data.get('quantidade')  * produto.preco) 
            itemCarrinho.quantidade = request.data.get('quantidade')
            print("AAAAAAAAA ANTES:", subtracao)
            itemCarrinho.subtotal -= subtracao
            itemCarrinho.save()
            print("AAAAAAAAA DEPOIS:", subtracao)
            carrinho.total -= subtracao
            carrinho.save()
        
        ItemCarrinhoSerializer = self.get_serializer(itemCarrinho)

        return response.Response(
            ItemCarrinhoSerializer.data 
            , status=status.HTTP_200_OK
            )
    