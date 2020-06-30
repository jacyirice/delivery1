from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DeleteView,CreateView,ListView,TemplateView

from .models import Prato,Categoria,Funcionario,Cliente,Pedido,Cliente, Endereco,PedidoPrato
from .forms import PratoForm,ClienteForm,CestaForm
# Create your views here.
def home(request):
	if request.user.is_authenticated:
		funcionario = Funcionario.objects.filter(usuario=request.user)
		if funcionario.exists():
			pratos=Prato.objects.all()
			return render(request, 'delivery/prato_list.html', {'object_list': pratos, 'is_funcionario': funcionario.exists() })
		else:
			categoria=Categoria.objects.all()
			pratos=[[],]
			pratos[0]=['Sugestões para você',Prato.objects.filter(sugestao=True)]

			for i in categoria:
				pratosCat=Prato.objects.filter(categoria=i)
				if pratosCat.exists():
					pratos.append([i.nome,pratosCat])

			return render(request,'delivery/prato_for_cliente.html',{'object_list':pratos})
	else:
		return redirect(reverse('erro'))

def carrinho(request):
	if request.user.is_authenticated:
		carrinho = PedidoPrato.objects.filter(pedido__cliente__usuario=request.user, pedido__status=0)
		if carrinho.exists():
			print(carrinho)
			return render(request,'delivery/carrinho.html',{'itens':carrinho,'total':carrinho[0].pedido.valor})
		else:
			messages.info(request, "Você ainda não adicionou nenhum item ao seu carrinho")
			return redirect(reverse('home'))
	else:
		return redirect(reverse('login'))


def adicionar_cesta(request, id_prato):
	if request.user.is_authenticated:
		cliente = Cliente.objects.filter(usuario=request.user)
		if cliente.exists():
			if request.method == 'GET':
				prato = Prato.objects.get(pk=id_prato)
				form = CestaForm(initial={'prato': prato.id})
				return render(request, 'delivery/carrinho_form.html', {'formulario': form, 'object': prato})


def carrinho_add(request):
	if request.method == 'GET':
		return redirect(reverse('carrinho'))				
	elif request.method == 'POST':
		cliente = Cliente.objects.filter(usuario=request.user)
		if cliente.exists():
			id_prato = request.POST['prato']
			quantidade = request.POST['quantidade']

			existe_pedido = Pedido.objects.filter(cliente=cliente[0], status=0)
			prato = Prato.objects.get(pk=id_prato)

			if not existe_pedido.exists():
				pedido = Pedido()
				pedido.cliente = cliente[0]
				pedido.status = 0  
				pedido.valor = float(request.POST['quantidade']) * prato.valor
				pedido.save()
			else:
				pedido = existe_pedido[0]
				pedido.valor += float(request.POST['quantidade']) * prato.valor				
				pedido.save()

			pp = PedidoPrato()
			pp.prato = prato
			pp.quantidade = request.POST['quantidade']
			pp.pedido = pedido
			pp.save()

			messages.success(request, "Item adicionado")
			return redirect(reverse('home'))
		return redirect(reverse('login'))

def carrinho_delete(request):
	if request.method == 'GET':
		return redirect(reverse('carrinho'))				
	elif request.method == 'POST':
		id_item = request.POST['id_item']
		item = PedidoPrato.objects.filter(pedido__cliente__usuario=request.user, pedido__status=0,pk=id_item)
		if item.exists():
			item.delete()
			messages.info(request, "Item deletado")
		else:
			messages.error(request, "Item não encontrado! Por favor, atualize a pagina.")
		return redirect(reverse('carrinho'))

def finalizarPedido(request):
	if request.method == 'GET':
		return redirect(reverse('carrinho'))				
	elif request.method == 'POST':
		cliente=get_object_or_404(Cliente,usuario=request.user)
		pedido = get_object_or_404(Pedido,status=0,cliente=cliente)
		pedido.status = 1
		pedido.save()
		messages.success(request, 'Pedido efetuado com sucesso! Você pode acompanhar o progresso na sessão Pedidos')
		return redirect(reverse('home'))

def pedidos_atendimentos(request):
	if request.user.is_authenticated:
		funcionario=get_object_or_404(Funcionario,usuario=request.user)
		pedidos = Pedido.objects.filter(status=1).order_by('-data_hora')
		atendimentos = Pedido.objects.filter(status=2).order_by('-data_hora')
		return render(request,'delivery/pedido_list.html',{'pedidos':pedidos,'atendimentos':atendimentos})
	else:
		return redirect(reverse('login'))

def entrega_list(request):
	if request.user.is_authenticated:
		funcionario=get_object_or_404(Funcionario,usuario=request.user)
		pedidos = Pedido.objects.filter(status=4).order_by('-data_hora')
		return render(request,'delivery/entrega_list.html',{'pedidos':pedidos})
	else:
		return redirect(reverse('login'))

def atender(request):
	if request.method == 'GET':
		return redirect(reverse('pedidos_list'))				
	elif request.method == 'POST':
		id=request.POST['id']
		funcionario=Funcionario.objects.get(usuario=request.user)
		pedido = Pedido.objects.get(pk=id)

		pedido.status=2
		pedido.save()

		messages.success(request, 'Atendimento em andamento!')
		return redirect(reverse('atender'))

def entregar(request):
	if request.method == 'GET':
		return redirect(reverse('pedidos_list'))				
	elif request.method == 'POST':
		id=request.POST['id']
		funcionario=Funcionario.objects.get(usuario=request.user)
		pedido =Pedido.objects.get(pk=id)		
		pedido.status=4
		pedido.save()

		messages.success(request, 'Entrega em andamento')
		return redirect(reverse('pedidos_list'))


class PratoDelete(LoginRequiredMixin,DeleteView):
	model = Prato
	def get_success_url(self):
		messages.success(self.request, 'Prato removido com sucesso!')
		return reverse('home')
	def get(self,request,pk):
		funcionario=get_object_or_404(Funcionario,usuario=request.user)
		object=Prato.objects.get(pk=pk)
		return render(request, 'delivery/prato_confirm_delete.html',{'object':object})

class PratoCreate(LoginRequiredMixin,CreateView):
	model = Prato
	form_class = PratoForm
	template_name='delivery/prato_form.html'
	def get_success_url(self):
		messages.success(self.request, 'Prato adicionado com sucesso!')
		return reverse('home')
	def get(self,request):
		funcionario=get_object_or_404(Funcionario,usuario=request.user)
		form = self.get_form()
		return render(request, self.template_name, {'form': form})

class PedidosClienteList(LoginRequiredMixin,ListView):
	template_name = 'delivery/pedidos_by_cliente.html'
	ordering='status','-data_hora'
	def get_queryset(self):
		self.cliente = get_object_or_404(Cliente,usuario=self.request.user)
		return Pedido.objects.filter(cliente=self.cliente).exclude(status=0)

class ClienteView(FormView):
	template_name = "delivery/cadastro_cliente.html"
	form_class = ClienteForm
	success_url=reverse_lazy('login')
	def form_valid(self, form):
		dados = form.clean()
		hash = make_password(dados['password'])
		usuario = User(username=dados['username'],password=hash, 
						email=dados['email'], first_name=dados['nome'],last_name=dados['sobrenome'])
		cliente = Cliente(usuario=usuario,cpf=dados['cpf'], telefone=dados['telefone'])
		endereco = Endereco(cep=dados['cep'],logradouro=dados['logradouro'],complemento=dados['complemento'],cliente=cliente)

		usuario.save()
		cliente.save()
		endereco.save()

		# grupoCliente=Group.objects.get(name = "Cliente")
		# usuario.groups.add(grupoCliente.pk)
		# usuario.save()
		
		return super().form_valid(form)

class ErroLoginTemplate(TemplateView):
	 template_name = "delivery/erro_login.html"