from rest_framework import serializers
from .models import Producto, Movimiento

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'codigo', 'stock', 'precio', 'categoria', 'categoria_nombre', 'fecha_creacion']



class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__' 