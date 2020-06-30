from django import forms
from .models import Categoria,Cliente,Endereco,Prato
from django.contrib.auth.models import User



class PratoForm(forms.ModelForm):
	class Meta:
		model = Prato
		fields = ['nome','descricao','valor','categoria','sugestao']
		widgets={
		'nome':forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'Nome'}),
		'categoria':forms.Select(attrs={'class': 'form-control pb-1', 'placeholder':'Categoria'}),
		'descricao':forms.Textarea(attrs={'class': 'form-control pb-1', 'placeholder':'Descrição'}),
		'valor':forms.NumberInput(attrs={'class': 'form-control pb-1', 'placeholder':'Valor'}),
		'sugestao':forms.CheckboxInput(attrs={'class': 'form-check-input pb-1'}),
		}
	def clean(self):
		dados = super().clean()
		nome = dados.get('nome',None)
		if nome:
			if len(Prato.objects.filter(nome=nome))!=0:
				self.add_error('nome', 'Esse prato ja esta cadastrado')
				self.fields['nome'].widget.attrs['class']+=' is-invalid'	
		valor = dados.get('valor',None)
		if valor:
			if valor<0.01:
				self.add_error('valor', 'Utilize um valor acima de R$ 0.01')
				self.fields['valor'].widget.attrs['class']+=' is-invalid'		
		return dados

class ClienteForm(forms.Form):	
	nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'Nome'}),max_length=128)
	sobrenome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'Sobrenome'}),max_length=140)
	cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'CPF'}),max_length=14)
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control pb-1', 'placeholder':'Email'}))
	telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1 ', 'placeholder':'Telefone'}),max_length=15)
	#user
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'Username'}),max_length=128)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pb-1', 'placeholder':'Password'}),max_length=128,min_length=8)
	#Endereço
	cep = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'CEP'}),max_length=15)
	logradouro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'Lougradouro'}),max_length=15)
	complemento = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pb-1', 'placeholder':'complemento'}),required=False)

	def clean(self):
		dados = super().clean()
		cpf=dados.get('cpf',None)
		if cpf:
			if Cliente.objects.filter(cpf=cpf).exists():
				self.add_error('cpf', 'Este CPF já foi cadastrado')
				self.fields['cpf'].widget.attrs['class']+=' is-invalid'
		email=dados.get('email',None)
		if email:
			if User.objects.filter(email=email).exists():
				self.add_error('email', 'Este email já foi cadastrado')
				self.fields['email'].widget.attrs['class']+=' is-invalid'
		username=dados.get('username',None)
		if username:
			if User.objects.filter(username=username).exists():
				self.add_error('username', 'Esse login esta indisponivel')
				self.fields['username'].widget.attrs['class']+=' is-invalid'
		return dados

class CestaForm(forms.Form):
    prato = forms.IntegerField(widget=forms.HiddenInput)
    quantidade = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control pb-1', 'placeholder':'Quantidade'}))