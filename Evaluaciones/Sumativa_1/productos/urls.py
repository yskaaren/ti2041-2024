from django.urls import path
from . import views


urlpatterns = [
    path('productos', views.product, name='productos'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('consultar/', views.consultar_productos, name='consultar_productos'),
    path('resultado/<int:producto_id>/', views.resultado_producto, name='resultado_producto'),

    
] 