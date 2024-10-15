from django.contrib import admin
from .models import Marca, Categoria, Producto, Caracteristica

admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Caracteristica)

