# La API está diseñada para gestionar los productos registrados en la base de datos, permite
# al usuario interactuar para realizar operaciones CRUD y está protegida mediante autenticación JWT
# para que solo los usuarios autorizados puedan realizar estas acciones.


from ninja import NinjaAPI, Schema
from productos.security import JWTBearer
from productos.models import Producto, Marca, Categoria
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
import random, string
from django.contrib.auth import authenticate

# Crear instancia de NinjaAPI con autenticación JWT
api = NinjaAPI()

# Schemas
class ProductoSchema(Schema):
    nombre: str
    precio: float
    marca: str
    categoria: str
    fecha_vencimiento: str

class AuthSchema(Schema):
    username: str
    password: str

#Nombre del servicio: POST /api/auth/login
#Este servicio permite autenticarse en la aplicación.
#Si las credenciales son válidas se genera un JWT de acceso y un refresh token.
#Entradas: Username y Password.
#Salidas: access_token, refresh_token y username.
@api.post("/auth/login", tags=["Auth"])
def login_user(request, data: AuthSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return {"error": "Usuario o contraseña incorrectos"}, 401
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "username": user.username,
    }

#Nombre del servicio: GET api/productos.
#Este servicio permite obtener la lista de todos los productos almacenados en la base de datos.
#Incluye información como nombre, precio, marca y categoría.
#Este servicio necesita que el usuario esté autenticado.
#Entrada: Autenticación JWT.
#Salidas: id, nombre, precio, marca_nombre, categoria_nombre.
@api.get("/productos", tags=["Productos"], auth=JWTBearer())
def listar_productos(request):
    productos = Producto.objects.all()
    return list(productos.values("id", "nombre", "precio", "marca__nombre", "categoria__nombre"))


#Nombre del Servicio: POST api/productos.
#Este servicio permite a los usuarios autenticados con el rol "ADMIN_PRODUCTS" para crear un nuevo producto.
#La solicitud debe incluir la información necesaria sobre el producto, como su nombre, precio, marca, categoría y fecha de vencimiento.
#Entradas: Autenticación JWT y solicitud JSON (nombre, precio, marca, categoría y fecha de vencimiento).
#Salidas: REspuesta exitosa, errores.
@api.post("/productos", tags=["Productos"], auth=JWTBearer())
def crear_producto(request, data: ProductoSchema):
    if not request.auth.groups.filter(name="ADMIN_PRODUCTS").exists():
        return {"error": "No tienes permisos para registrar productos"}, 403

    fecha_vencimiento = datetime.strptime(data.fecha_vencimiento, "%Y-%m-%d").date()
    marca, _ = Marca.objects.get_or_create(nombre=data.marca)
    categoria, _ = Categoria.objects.get_or_create(nombre=data.categoria)

    codigo = generar_codigo_producto()
    producto = Producto(
        codigo=codigo,
        nombre=data.nombre,
        precio=data.precio,
        marca=marca,
        categoria=categoria,
        fecha_vencimiento=fecha_vencimiento,
    )
    producto.save()
    return {"message": "Producto creado exitosamente", "id": producto.id}


#Nombre del servicio: GET /api/productos/{producto_id}.
#Este servicio permite obtener los detalles de un producto mediante su ID.
#La solicitud debe incluir el ID del producto.
#Entradas: Autenticación JWT, ID del producto.
#Salidas: Respuesta exitosa, Errores.
@api.get("/productos/{producto_id}", tags=["Productos"], auth=JWTBearer())
def obtener_producto(request, producto_id: int):
    producto = Producto.objects.filter(id=producto_id).first()
    if not producto:
        raise Http404("Producto no encontrado")
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "marca": producto.marca.nombre,
        "categoria": producto.categoria.nombre,
    }


#Nombre del servicio: PUT /api/productos/{producto_id}.
#Este servicio permite actualizar los detalles de un producto existente.
#Se debe proporcionar el ID del producto y los nuevos valores.
#Entradas: Autenticación JWT, ID del producto, Nuevos valores.
#Salidas: Respuesta exitosa, Errores.
@api.put("/productos/{producto_id}", tags=["Productos"], auth=JWTBearer())
def actualizar_producto(request, producto_id: int, data: ProductoSchema):
    producto = Producto.objects.filter(id=producto_id).first()
    if not producto:
        raise Http404("Producto no encontrado")

    producto.nombre = data.nombre
    producto.precio = data.precio
    producto.marca, _ = Marca.objects.get_or_create(nombre=data.marca)
    producto.categoria, _ = Categoria.objects.get_or_create(nombre=data.categoria)
    producto.fecha_vencimiento = datetime.strptime(data.fecha_vencimiento, "%Y-%m-%d").date()
    producto.save()

    return {"message": "Producto actualizado exitosamente"}

#Nombre del servicio: DELETE /api/productos/{producto_id}.
#Este servicio permite eliminar un producto existente.
#Se debe proporcionar el ID del producto.
#Entradas: Autenticación JWT, ID del producto.
#Salidas: Respuesta exitosa, Errores.
@api.delete("/productos/{producto_id}", tags=["Productos"], auth=JWTBearer())
def eliminar_producto(request, producto_id: int):
    producto = Producto.objects.filter(id=producto_id).first()
    if not producto:
        raise Http404("Producto no encontrado")

    producto.delete()
    return {"message": "Producto eliminado exitosamente"}

#Nombre del servicio: generar_codigo_producto.
#Este servicio genera un codigo unico de 6 caracteres al azar, con letras mayusculas y numeros (0-9).
#El código generado se asegura de ser único verificando si ya existe en la base de datos para el modelo Producto.
#Entrada: No requiere entrada desde el usuario o desde la API.
#Salidas: La salida es un código único compuesto por 6 caracteres aleatorios (letras y números).
def generar_codigo_producto():
    letras = string.ascii_uppercase
    numeros = string.digits
    codigo = ''.join(random.choices(letras + numeros, k=6))
    while Producto.objects.filter(codigo=codigo).exists():
        codigo = ''.join(random.choices(letras + numeros, k=6))
    return codigo

