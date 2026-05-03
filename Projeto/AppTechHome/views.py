from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Produto, Pedido, Suporte
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, View
from .forms import *
from django.db.models import Sum, F
# Create your views here.


    



class ProdutoHomeView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'Tela1Home.html'
    paginate_by = 10
    context_object_name = 'produto'

    def get_queryset(self):
        queryset = Produto.objects.all()
        busca = self.request.GET.get('barra')
        
        if busca:
            queryset = queryset.filter(nome__icontains=busca)

        
        return queryset
    
class ProdutoDetalhe(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'Tela4Detalhes.html'
    context_object_name = 'produto'


    
    
class ProdutoCategoriaView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'Tela3Categoria.html'
    paginate_by = 3
    context_object_name = 'produto'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categorias = self.request.GET.get('categoria')
        pagina = self.request.GET.get('buscar')

        if pagina:
            queryset = queryset.filter(nome__icontains=pagina)

        if categorias:
                queryset = queryset.filter(categoria__nome=categorias)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        return context
class ProdutoPagamento(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'Tela5Pagamento.html'
    context_object_name = 'produto'

    
class ProdutoFinalizacao(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = 'Tela5Pagamento.html'
    context_object_name = 'produto'
    success_url = reverse_lazy('home')

    def post(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk)


        pagamento = Pedido.objects.create(
            nome=request.POST.get('nome_completo'),
            email=request.POST.get('email'),
            cpf=request.POST.get('cpf'),
            rua=request.POST.get('rua'),
            cidade=request.POST.get('cidade'),
            estado=request.POST.get('estado')
        )
        
        pagamento.save()

        if produto.estoque > 0:
            produto.estoque -= 1
            produto.save()
        else:
            print("Produto sem estoque")
        return redirect('home')
    


class Contato(LoginRequiredMixin, CreateView):
    model = Suporte
    template_name = 'Tela2_Contato.html'
    context_object_name = 'contato'
    fields = ['nome', 'motivo', 'mensagem']
    success_url = reverse_lazy('home')

    def post(self, request):
        


        contato = Suporte.objects.create(
            nome=request.POST.get('nome'),
            motivo=request.POST.get('assunto'),
            mensagem=request.POST.get('mensagem'),
            
        )
        
        contato.save()
            
        return redirect('home')
    


class Perfil(LoginRequiredMixin, TemplateView):
    template_name = 'Tela7Perfil.html'

    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
    
    
        contexto['gerente'] = self.request.user.groups.filter(name='Gerente').exists()

        return contexto

class Gerenciador(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'Tela8Gerenciamento.html'
    context_object_name = 'produto'

class GerenciadorCate(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'Tela13GerenciamentoCate.html'
    context_object_name = 'categoria'    

    def get_queryset(self):
        categoria = super().get_queryset()

        buscar = self.request.GET.get('buscar')
        

        if buscar:
            categoria = categoria.filter(nome__icontains=buscar)

        return categoria
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = context['categoria']

        context['total_produto'] = categoria.count()

        return context 
class GerenciadorProd(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'Tela12GerenciamentoProd.html'
    context_object_name = 'produto'

    def get_queryset(self):
        produtos = super().get_queryset()

        buscar = self.request.GET.get('buscar')
        

        if buscar:
            produtos = produtos.filter(nome__icontains=buscar)

        return produtos
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto = context['produto']

        context['total_produto'] = produto.count()


        context['itens_estoque'] = produto.aggregate(
            total_estoque=Sum('estoque')
        )['total_estoque'] or 0

        context['valor_total'] = produto.aggregate(
            total=Sum(F('preco') * F('estoque'))
        )['total'] or 0

        for p in produto:
            p.total = p.preco * p.estoque

        return context  

class AdicionarProduto(LoginRequiredMixin, CreateView):
    form_class = ProdutoForm
    template_name = 'Tela9Adicionar.html'
    success_url = reverse_lazy('gerenciadoPro')


class AdicionarCategoria(LoginRequiredMixin, CreateView):
    form_class = CategoriaForm
    template_name = 'Tela11AdicionarCatego.html'
    success_url = reverse_lazy('gerenciadoCate')


class EditarCategoria(LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nome']
    template_name = 'Tela14EditarCate.html'
    success_url = reverse_lazy('gerenciadoCate')

class EditarProduto(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome', 'imagem', 'descricao', 'estoque', 'preco', 'categoria']
    template_name = 'Tela10Editar.html'
    success_url = reverse_lazy('gerenciadoPro')
    

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        return super().post(request, *args, **kwargs)


def remover_categoria(request:HttpRequest, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect("gerenciadoCate")

def remover_produto(request:HttpRequest, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect("gerenciadoPro")
