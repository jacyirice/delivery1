from django.contrib import admin
from .models import Endereco,Cliente,Categoria,Prato,Pedido, Funcionario
# Register your models here.

@admin.register(Endereco)
class Endereco(admin.ModelAdmin):
    pass
@admin.register(Cliente)
class Cliente(admin.ModelAdmin):
    pass
@admin.register(Funcionario)
class Funcionario(admin.ModelAdmin):
    pass
@admin.register(Categoria)
class Categoria(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
@admin.register(Prato)
class Prato(admin.ModelAdmin):
    pass
@admin.register(Pedido)
class Pedido(admin.ModelAdmin):
    pass

