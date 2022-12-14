from django.contrib import admin
from django.urls import path, include
from cadastro.views import *

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from django.conf.urls.static import static


schema = get_schema_view(
   openapi.Info(
      title="HennerAPI",
      default_version='v0.1',
      description="API Lojas Henner."),
    public=True,
    permission_classes=[permissions.AllowAny],
    )



router = routers.DefaultRouter()
router.register(r'cliente', ClientesViewSet, basename = 'clientes')
router.register(r'endereco', EnderecosViewSet, basename = 'enderecos')
router.register(r'item-carrinho', ItemCarrinhoViewSet, basename = 'item_carrinho')
router.register(r'produtos', ProdutosViewSet , basename = 'produtos')
router.register(r'categoria', CategoriaViewSet , basename = 'categoria')
router.register(r'unidade-federativa', UnidadeFederativaViewSet , basename = 'unidade_federativa')
router.register(r'municipio', MunicipioViewSet , basename = 'municipio')
router.register(r'cartao', CartaoViewSet , basename = 'cartao')
router.register(r'pedido', PedidoViewSet , basename = 'pedido')
router.register(r'carrinho', CarrinhoViewSet , basename = 'carrinho')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('',include(router.urls) ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
