"""restaurante URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (home,
					ErroLoginTemplate,
					ClienteView,
					PedidosClienteList,
					PratoCreate,
					PratoDelete,
					carrinho,
					carrinho_add,
					carrinho_delete,
					finalizarPedido,
                    pedidos_atendimentos,
					atender,
					entregar,
					entrega_list,
					adicionar_cesta)
urlpatterns = [
	path('', home, name='home'),
	path('erro-login/', ErroLoginTemplate.as_view(), name='erro'),
	path('cliente/cadastro/', ClienteView.as_view(), name='cadastroCliente'),
    path('cliente/pedidos/', PedidosClienteList.as_view(), name='pedidos_by_cliente'),

	path('prato/adicionar/', PratoCreate.as_view(), name='prato-add'),
	path('prato/<int:pk>/delete/', PratoDelete.as_view(), name='prato-delete'),

	path('carrinho/', carrinho, name='carrinho'),
	path('carrinho/adicionar/<int:id_prato>', adicionar_cesta, name='adicionar-car-get'),
	path('carrinho/adicionar/', carrinho_add, name='carrinho-add'),
	path('carrinho/deletar/', carrinho_delete, name='carrinho-delete'),
	path('carrinho/finalizar/', finalizarPedido, name='finalizarPedido'),

	path('pedidos/', pedidos_atendimentos, name='pedidos_list'),
	path('pedidos/atender/', atender, name='atender'),
	path('pedidos/entregar/', entregar, name='entregar'),
	path('entregas/', entrega_list, name='entrega_list'),
]
