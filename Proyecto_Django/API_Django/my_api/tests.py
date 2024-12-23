from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Producto, Movimiento

class ProductoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.producto_data = {'nombre': 'Producto 1', 'descripcion': 'Descripción del producto 1', 'precio': 10.00, 'stock': 100}
        self.response = self.client.post('/api/productos/', self.producto_data, format='json')

    def test_crear_producto(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_obtener_producto(self):
        producto = Producto.objects.get()
        response = self.client.get(f'/api/productos/{producto.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, producto.nombre)

    def test_actualizar_producto(self):
        producto = Producto.objects.get()
        nuevo_dato = {'nombre': 'Producto Actualizado', 'descripcion': 'Descripción actualizada', 'precio': 20.00, 'stock': 50}
        response = self.client.put(f'/api/productos/{producto.id}/', nuevo_dato, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_producto(self):
        producto = Producto.objects.get()
        response = self.client.delete(f'/api/productos/{producto.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)