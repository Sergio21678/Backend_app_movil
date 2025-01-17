import uuid
from django.db import models

# Modelo para las categorías de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la categoría
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional

    class Meta:
        db_table = 'categorias'  # Nombre de la tabla en la base de datos

    def __str__(self):
        return self.nombre # Representación en texto de la categoría


# Modelo para los productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100) # Nombre del producto
    descripcion = models.TextField() # Descripción del producto
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Código único del producto
    stock = models.IntegerField() # Cantidad en stock
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Precio del producto
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True) # Relación con categoría
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Fecha de creación

    class Meta:
        db_table = 'productos'  # Nombre de la tabla en la base de datos
    
    def __str__(self):
        return self.nombre  # Representación en texto del producto

    def save(self, *args, **kwargs):
        # Generar automáticamente un código único si no se ha proporcionado
        if not self.codigo:
            self.codigo = f'P{uuid.uuid4().hex[:8].upper()}'  # Ejemplo: P5F3D2A1B
        super().save(*args, **kwargs)

# Modelo para los movimientos de inventario (entrada/salida/ajuste)
class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # Relación con producto
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES) # Tipo de movimiento
    cantidad = models.IntegerField() # Cantidad movida
    fecha = models.DateTimeField(auto_now_add=True) # Fecha del movimient

    class Meta:
        db_table = 'movimientos_inventario'
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
