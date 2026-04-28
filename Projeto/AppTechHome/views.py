from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from httpcore import request
from .models import Produto, Pedido, Suporte
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, View
from .forms import *
# Create your views here.


    



class ProdutoHomeView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'Tela1Home.html'
    context_object_name = 'produto'

    def get_queryset(self):
        queryset = Produto.objects.all()
        busca = self.request.GET.get('barra')
        
        if busca:
            queryset = queryset.filter(nome__icontains=busca)

        
        return queryset
    
class ProdutoDetalhe(DetailView):
    model = Produto
    template_name = 'Tela4Detalhes.html'
    context_object_name = 'produto'


    
    
class ProdutoCategoriaView(ListView):
    model = Produto
    template_name = 'Tela3Categoria.html'
    paginate_by = 5
    context_object_name = 'produto'
    
    def get_queryset(self):
        queryset = Produto.objects.all()
        categorias = self.request.GET.get('categoria')
        if categorias:
                queryset = queryset.filter(categoria__nome=categorias)
        
        return queryset
    
class ProdutoPagamento(DetailView):
    model = Produto
    template_name = 'Tela5Pagamento.html'
    context_object_name = 'produto'

    
class ProdutoFinalizacao(CreateView):
    model = Produto
    template_name = 'Tela1Home.html'
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
    

class SuporteView(ListView):
    model = Suporte
    template_name = 'Tela2_Contato.html'
    context_object_name = 'suporte'

class Contato(CreateView):
    model = Suporte
    template_name = 'Tela1Home.html'
    context_object_name = 'contato'
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


class AdicionarProduto(LoginRequiredMixin, CreateView):
    form_class = ProdutoForm
    template_name = 'Tela9Adicionar.html'
    success_url = reverse_lazy('gerenciador')

    
class EditarProduto(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome', 'imagem', 'descricao', 'estoque', 'preco', 'categoria']
    template_name = 'Tela10Editar.html'
    success_url = reverse_lazy('gerenciador')
    

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        return super().post(request, *args, **kwargs)

def remover_produto(request:HttpRequest, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect("gerenciador")
