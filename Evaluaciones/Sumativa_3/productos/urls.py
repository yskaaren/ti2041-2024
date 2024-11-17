from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_app, name='login'),
    path('', views.login_app, name='root'),
    path('index/', views.product, name='index'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('consultar/', views.consultar_productos, name='consultar_productos'),
    path('resultado/<int:producto_id>/', views.resultado_producto, name='resultado_producto'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
] 