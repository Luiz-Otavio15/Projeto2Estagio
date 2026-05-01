
from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='Tela6Login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='sair'),
    path('principal/', ProdutoHomeView.as_view(), name='home'),
    path('produto/<int:pk>/', ProdutoDetalhe.as_view(), name='detalhe_produto'),
    path('categoria/', ProdutoCategoriaView.as_view(), name='categoria_produto'),
    path('pagamento/<int:pk>/', ProdutoPagamento.as_view(), name='pagamento_produto'),
    path('finalizacao/<int:pk>/', ProdutoFinalizacao.as_view(), name='finalizacao'),
    path('contato/', Contato.as_view(), name='contato'),
    path('perfil/', Perfil.as_view(), name='perfil'),
    path('gerenciador/', Gerenciador.as_view(), name='gerenciador'),
    path('gerenciadorCate/', GerenciadorCate.as_view(), name='gerenciadoCate'),
    path('gerenciadoPro/', GerenciadorProd.as_view(), name='gerenciadoPro' ),
    path('addProduto/', AdicionarProduto.as_view(), name='adicionar'),
    path('addCategoria/', AdicionarCategoria.as_view(), name='adicategoria'),
    path('delete/<int:id>', remover_produto, name='deletar'),
    path('deleteCate/<int:id>', remover_categoria, name='deletarCate'),
    path('editar/<int:pk>', EditarProduto.as_view(), name='editar'),
    path('editarCate/<int:pk>', EditarCategoria.as_view(), name="editarCate"),
]
