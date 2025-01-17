from django.contrib import admin
from .models import Producto, Movimiento, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('nombre',)
    ordering = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'fecha_creacion')
    search_fields = ('nombre', 'categoria__nombre')
    list_filter = ('categoria', 'fecha_creacion')
    ordering = ('nombre',)


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha')
    search_fields = ('producto__nombre',)
    list_filter = ('tipo', 'fecha')