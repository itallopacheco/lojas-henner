from django.http import JsonResponse
from cadastro.serializer import ClientesSerializer
from rest_framework import viewsets
from cadastro.models import Cliente


# Create your views here.

class ClientesViewSet(viewsets.ModelViewSet):
    """ Exibindo todos os Clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClientesSerializer

