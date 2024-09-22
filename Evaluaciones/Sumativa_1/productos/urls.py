from django.urls import path
from . import views


urlpatterns = [
    path('productos', views.product),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('consultar_productos/', views.consultar_productos, name='consultar_productos'),
]