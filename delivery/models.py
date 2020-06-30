from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	cpf = models.CharField(max_length=11)
	telefone = models.CharField('Telefone', max_length=15,
										 help_text='Número do telefone celular no formato (99) 99999-9999')
	def __str__(self):
		return self.usuario.first_name

class Endereco(models.Model):
	cep = models.CharField('CEP',max_length=9)
	logradouro = models.CharField('Lougradouro',max_length=15)
	complemento = models.CharField('Complemento',max_length=10, blank=True, null=True)
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

	def __str__(self):
		return '{} - {}'.format(self.cep, self.descricao)

class Funcionario(models.Model):
	nome = models.CharField(max_length=120)
	matricula = models.CharField(max_length=6)
	cargo = models.CharField(max_length=60)
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)	

	def __str__(self):
		return '{} - {}'.format(self.matricula, self.nome)

class Categoria(models.Model):
	nome = models.CharField('Nome',max_length=150)
	slug = models.SlugField(max_length=150)
	def __str__(self):
		return self.nome

class Prato(models.Model):
	nome = models.CharField(max_length=50)
	descricao = models.TextField()
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	valor = models.FloatField()
	sugestao=models.BooleanField(default=False)

	def __str__(self):
		return '{} - {}'.format(self.nome, str(self.valor))


class Pedido(models.Model):
	STATUS_PEDIDO = [
		(0, 'Sendo criado'),
		(1, 'Em espera'),
		(2, 'Em produção'),
		(3, 'Cancelado'),
		(4, 'Saiu para entrega'),
		(5, 'Finalizado'),
	]
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	status = models.SmallIntegerField(choices=STATUS_PEDIDO)
	valor = models.FloatField()
	data_hora = models.DateTimeField(auto_now_add=True,null=True)
	def __str__(self):
		return '{} - {} - {}'.format(self.pk, self.cliente, self.status)


class PedidoPrato(models.Model):
	prato = models.ForeignKey(Prato, on_delete=models.CASCADE)
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
	quantidade = models.IntegerField()