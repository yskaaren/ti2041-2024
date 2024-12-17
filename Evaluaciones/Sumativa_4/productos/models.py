from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.codigo}"

class Caracteristica(models.Model):
    producto = models.ForeignKey(Producto, related_name="caracteristicas", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}: {self.valor}"