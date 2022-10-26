from django.contrib import admin
from .models import Cliente, Endereco, UnidadeFederativa, Municipio, Cartao



class Clientes(admin.ModelAdmin):
    list_display = ('id','primeiro_nome', 'ultimo_nome', 'data_nascimento', 'cpf', 'email')
    list_filter = ('primeiro_nome', 'ultimo_nome', 'data_nascimento', 'cpf', 'email')
    search_fields = ('primeiro_nome', 'ultimo_nome', 'cpf', 'email')
    ordering = (['id'])
    list_display_links = ('id','cpf')
    filter_horizontal = ()
    list_per_page = 25

admin.site.register(Cliente, Clientes)

class Enderecos(admin.ModelAdmin):
    list_display = ('id','cidade','estado','rua','bairro')
    list_filter = ('estado','rua','bairro')
    search_fields = ('cidade__name','estado','rua','bairro')
    ordering = (['id'])
    list_display_links = ('id','cidade')
    filter_horizontal = ()
    list_per_page = 25

admin.site.register(Endereco, Enderecos)

class UnidadesFederativas(admin.ModelAdmin):
    list_display = ('sigla','nome')
    list_filter = ('sigla','nome')
    search_fields = ('sigla__name','nome')
    ordering = ([])
    filter_horizontal = ()
    list_per_page = 25

admin.site.register(UnidadeFederativa, UnidadesFederativas)

class Municipios(admin.ModelAdmin):
    list_display = ('nome','estado')
    list_filter = ('nome','estado')
    search_fields = ('nome','estado__nome')
    ordering = ([])
    filter_horizontal = ()
    list_per_page = 25

admin.site.register(Municipio, Municipios)

class Cartoes(admin.ModelAdmin):
    list_display = ('id','numero','nome','validade','codigo')
    list_filter = ('numero','nome','validade','codigo')
    search_fields = ('numero','nome','validade','codigo')
    ordering = (['id'])
    list_display_links = ('id','numero')
    filter_horizontal = ()
    list_per_page = 25

admin.site.register(Cartao, Cartoes)