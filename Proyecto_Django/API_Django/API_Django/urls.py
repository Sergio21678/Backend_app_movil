from django.contrib import admin
from django.urls import path
from my_api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from my_api.views import CustomTokenRefreshView
from my_api.views import ProductoBusquedaAvanzadaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/productos/', views.ProductoListCreateView.as_view(), name='producto_list_create'),
    path('api/productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('api/movimientos/', views.MovimientoListCreateView.as_view(), name='movimiento_list_create'),
    path('api/movimientos/<int:pk>/', views.MovimientoDetailView.as_view(), name='movimiento_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/productos/busqueda/', ProductoBusquedaAvanzadaView.as_view(), name='producto_busqueda_avanzada'),
]