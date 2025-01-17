from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Producto, Movimiento, Categoria
from .serializers import ProductoSerializer, MovimientoSerializer, CategoriaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
import logging
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, ListAPIView

# Logger para registrar información en la consola
logger = logging.getLogger(__name__)

# Listar y crear productos
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all().select_related('categoria') # Consulta optimizada
    serializer_class = ProductoSerializer # Define el serializador a usar
    permission_classes = [IsAuthenticated] # Requiere autenticación

    # Método para crear un producto solo si el usuario es administrador
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permisos para crear productos")

# Vista para obtener o actualizar un producto
class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

# Vista para listar y crear movimientos
class MovimientoListCreateView(ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

    # Validación para crear movimientos solo si es administrador
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para realizar esta acción.")
# Vista para detalle y actualización de movimientos
class MovimientoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] # Solo admins pueden modificar

# Vista protegida de prueba
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Esto está protegido"})
    
# Vista personalizada para refrescar el token
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Datos recibidos: {request.data}")
        return super().post(request, *args, **kwargs)
    
# Vista para búsqueda avanzada de productos
class ProductoBusquedaAvanzadaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nombre = request.query_params.get('nombre', None)
        categoria = request.query_params.get('categoria', None)
        precio_min = request.query_params.get('precio_min', None)
        precio_max = request.query_params.get('precio_max', None)

        filtros = Q()
        if nombre:
            filtros &= Q(nombre__icontains=nombre)
        if categoria:
            filtros &= Q(categoria__nombre__icontains=categoria)
        if precio_min:
            filtros &= Q(precio__gte=precio_min)
        if precio_max:
            filtros &= Q(precio__lte=precio_max)

        productos = Producto.objects.filter(filtros)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

# Vista para búsqueda de movimientos
class MovimientoListCreateView(ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            movimiento = serializer.save()
            producto = movimiento.producto

            # Actualiza el stock del producto según el tipo de movimiento
            if movimiento.tipo == 'entrada':
                producto.stock += movimiento.cantidad
            elif movimiento.tipo == 'salida':
                if producto.stock < movimiento.cantidad:
                    raise PermissionDenied("No hay suficiente stock para realizar esta salida.")
                producto.stock -= movimiento.cantidad
            else:
                raise PermissionDenied("Tipo de movimiento no válido.")

            producto.save()
        else:
            raise PermissionDenied("No tienes permiso para realizar esta acción.")

# Vista para obtener productos por código
class MovimientoBusquedaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        producto_nombre = request.query_params.get('producto_nombre', None)
        tipos = request.query_params.getlist('tipo', None)  # Permite seleccionar múltiples tipos
        cantidad = request.query_params.get('cantidad', None)  # Cantidad exacta
        fecha = request.query_params.get('fecha', None)  # Fecha exacta

        filtros = Q()

        # 🔎 Filtro por nombre de producto
        if producto_nombre:
            filtros &= Q(producto__nombre__icontains=producto_nombre)

        # 🔎 Filtro por tipo (entrada, salida)
        if tipos:
            filtros &= Q(tipo__in=tipos)

        # 🔎 Filtro por cantidad exacta
        if cantidad:
            filtros &= Q(cantidad=cantidad)

        # 🔎 Filtro por fecha exacta
        if fecha:
            filtros &= Q(fecha__date=fecha)

        # Consulta a la base de datos
        movimientos = Movimiento.objects.filter(filtros)
        serializer = MovimientoSerializer(movimientos, many=True)
        return Response(serializer.data)

# Búsqueda de productos por código
class ProductoPorCodigoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, codigo):
        try:
            producto = Producto.objects.get(codigo=codigo)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)


class CategoriaListView(ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer