from ninja import NinjaAPI
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from productos.models import Producto, Marca, Categoria, Caracteristica
from ninja.security import HttpBearer
import random, string
from datetime import datetime

api = NinjaAPI()

# Servicio: Inicio de sesión
@api.post("/login")
def login_app(request, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return {
            "message": "Inicio de sesión exitoso",
            "username": user.username,
        }
    return {"error": "Usuario o contraseña incorrectos"}, 401

# Servicio: Consultar productos
@api.get("/productos")
def consultar_productos(request, marca: int = None, categoria: int = None, caracteristica: str = None):
    productos = Producto.objects.all()
    if marca:
        productos = productos.filter(marca_id=marca)
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    if caracteristica:
        productos = productos.filter(caracteristicas__nombre=caracteristica).distinct()
    return list(productos.values("id", "nombre", "precio", "marca__nombre", "categoria__nombre"))

# Servicio: Registrar un producto
@api.post("/productos")
def registrar_producto(request, nombre: str, precio: float, marca: str, categoria: str, fecha_vencimiento: str):
    # Verifica permisos
    if not request.user.groups.filter(name="ADMIN_PRODUCTS").exists():
        return {"error": "No tienes permisos para registrar productos"}, 403

    try:
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Fecha de vencimiento no válida"}, 400

    marca_obj, _ = Marca.objects.get_or_create(nombre=marca)
    categoria_obj, _ = Categoria.objects.get_or_create(nombre=categoria)

    codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    producto = Producto(
        codigo=codigo,
        nombre=nombre,
        precio=precio,
        marca=marca_obj,
        categoria=categoria_obj,
    )
    producto.save()

    return {"message": "Producto registrado", "id": producto.id}

# Servicio: Cerrar sesión
@api.post("/logout")
def logout_view(request):
    logout(request)
    return {"message": "Cierre de sesión exitoso"}
