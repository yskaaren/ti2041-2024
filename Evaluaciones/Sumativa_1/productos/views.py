import random
import string
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Producto, Marca, Categoria, Caracteristica
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_app(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

@login_required
def product(request):
    return render(request, 'index.html')

@login_required
def consultar_productos(request):
    productos = Producto.objects.all()
    
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()

    marca_id = request.GET.get('marca', None)
    if marca_id:
        productos = productos.filter(marca_id=int(marca_id))

    categoria_id = request.GET.get('categoria', None)
    if categoria_id:
        productos = productos.filter(categoria_id=int(categoria_id))

    caracteristica_nombre = request.GET.get('caracteristica', None)
    if caracteristica_nombre:
        productos = productos.filter(caracteristicas__nombre=caracteristica_nombre).distinct()

    return render(request, 'consulta.html', {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
    })

@login_required
def generar_codigo_producto():
    letras = string.ascii_uppercase
    numeros = string.digits
    codigo = ''.join(random.choices(letras + numeros, k=6))

    while Producto.objects.filter(codigo=codigo).exists():
        codigo = ''.join(random.choices(letras + numeros, k=6))
    
    return codigo

@login_required
def registrar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca_nombre = request.POST.get('marca')
        categoria_nombre = request.POST.get('categoria')
        precio = request.POST.get('precio')
        fecha_vencimiento_str = request.POST.get('fecha_vencimiento')

        if not nombre or not precio or not fecha_vencimiento_str:
            return render(request, 'productos/registro.html', {
                'error': 'Todos los campos son obligatorios',
                'marca': Marca.objects.all(),
                'categoria': Categoria.objects.all(),
            })

        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'productos/registro.html', {
                'error': 'La fecha de vencimiento no es válida.',
                'marca': Marca.objects.all(),
                'categoria': Categoria.objects.all(),
            })
        
        marca, created = Marca.objects.get_or_create(nombre=marca_nombre)

        categoria, created = Categoria.objects.get_or_create(nombre=categoria_nombre)

        codigo = generar_codigo_producto()

        producto = Producto(
            codigo=codigo, 
            nombre=nombre,
            precio=precio,
            marca=marca,
            categoria=categoria,
        )
        producto.save()

        nombres_caracteristicas = request.POST.getlist('caracteristica_nombre[]')
        valores_caracteristicas = request.POST.getlist('caracteristica_valor[]')

        for nombre, valor in zip(nombres_caracteristicas, valores_caracteristicas):
            if nombre and valor:
                Caracteristica.objects.create(producto=producto, nombre=nombre, valor=valor)

        return redirect('resultado_producto', producto_id=producto.id)
    
    return render(request, 'registro.html', {
        'marca': Marca.objects.all(),
        'categoria': Categoria.objects.all(),
    })

@login_required
def mostrar_productos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'resultado.html', {'producto': producto})

def resultado_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'resultado.html', {'producto': producto})