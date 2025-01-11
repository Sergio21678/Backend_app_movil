from rest_framework import serializers
from .models import Producto, Movimiento

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'codigo', 'stock', 'precio', 'categoria', 'categoria_nombre', 'fecha_creacion']



class MovimientoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = Movimiento
        fields = ['id', 'producto', 'producto_nombre', 'tipo', 'cantidad', 'fecha']
        extra_kwargs = {
            'producto': {'required': True},  # Es obligatorio
        }
