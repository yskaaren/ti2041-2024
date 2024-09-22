from django.shortcuts import render, redirect
from django.utils import timezone

productos_memoria = []

# Create your views here.

def product(request):
    print("Productos")

    return render(request, 'index.html')

def registrar_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        nuevo_producto = {
            'codigo': codigo,
            'nombre': nombre,
            'marca': marca,
            'fecha_vencimiento': fecha_vencimiento,
        }
        productos_memoria.append(nuevo_producto)

        return render(request, 'resultado.html', {'producto': nuevo_producto})

    return render(request, 'registro.html')

def consultar_productos(request):
    return render(request, 'consulta.html', {'productos': productos_memoria})