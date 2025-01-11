from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Producto, Movimiento
from .serializers import ProductoSerializer, MovimientoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
import logging
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView

logger = logging.getLogger(__name__)

class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all().select_related('categoria')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permisos para crear productos")

class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class MovimientoListCreateView(ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para realizar esta acción.")

class MovimientoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Esto está protegido"})
    

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Datos recibidos: {request.data}")
        return super().post(request, *args, **kwargs)
    

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
