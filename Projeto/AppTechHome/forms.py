from django import forms
from .models import *


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'estoque', 'preco', 'categoria', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-text'}),
            'descricao': forms.TextInput(attrs={'class': 'input-text'}),
            'estoque': forms.NumberInput(attrs={'class': 'input-text'}),
            'preco': forms.NumberInput(attrs={'class': 'input-text'}),
            'categoria': forms.Select(attrs={'class': 'input-text'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'input-text'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']   
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-text'})
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nome', 'email', 'cpf', 'rua', 'cidade', 'estado']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-text'}),
            'email': forms.EmailInput(attrs={'class': 'input-text'}),
            'cpf': forms.TextInput(attrs={'class': 'input-text'}),
            'rua': forms.TextInput(attrs={'class': 'input-text'}),
            'cidade': forms.TextInput(attrs={'class': 'input-text'}),
            'estado': forms.TextInput(attrs={'class': 'input-text'}),
        }