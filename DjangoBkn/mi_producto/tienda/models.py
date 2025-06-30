from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.decorators import login_required


def validar_precio_minimo(valor):
    if valor < 1000000:
        raise ValidationError('El precio mínimo debe ser de 1.000.000 pesos.')
    
def validar_precio_rep(valor):
    if valor < 5000:
        raise ValidationError('El precio mínimo debe ser de 5.000 pesos.')
    
def validar_mayor_pr(valor):
    if valor < 3000000:
        raise ValidationError('El precio mínimo debe ser de 3.000.000 pesos.')
    
def validar_mayor_rep(valor):
    if valor < 10000:
        raise ValidationError('El precio mínimo debe ser de 10.000 pesos.')
    



class Producto(models.Model):
    nombre = models.CharField(max_length=1000)
    descrip = models.CharField(max_length=1000)
    precio = models.IntegerField(validators=[validar_precio_minimo])
    es_publico = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='productos_creados')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='productos_modificados')
    precio_mayorista = models.IntegerField(validators=[validar_mayor_pr], default=0)
    categoria = models.ForeignKey('CategoriaProducto', on_delete=models.SET_NULL, null=True, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    nombre = models.CharField(max_length=1000)
    descrip = models.CharField(max_length=1000)
    precio = models.IntegerField(validators=[validar_precio_rep])
    es_publico = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='repuestos')
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='repuestos_creados')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='repuestos_modificados')
    precio_mayorista = models.IntegerField(validators=[validar_mayor_rep], default=0)
    categoria = models.ForeignKey('CategoriaRepuesto', on_delete=models.SET_NULL, null=True, related_name='repuestos')
    imagen = models.ImageField(upload_to='repuestos/', null=True, blank=True)  # Nuevo campo para imágenes
    destacado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nombre} (para {self.producto.nombre})"

    
class UsuarioNormal(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    rut = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{7,8}-[0-9kK]$', 'Ingrese un RUT válido.')]
    )
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"
    
class UsuarioEmpresa(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nombre_empresa = models.CharField(max_length=255)
    rut_empresa = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{7,8}-[0-9kK]$', 'Ingrese un RUT válido.')]
    )
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.nombre_empresa}"

class CategoriaProducto(models.Model):
        nombre = models.CharField(max_length=255)

        def __str__(self):
            return self.nombre
    
class CategoriaRepuesto(models.Model):
        nombre = models.CharField(max_length=255)

        def __str__(self):
            return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carritos')
    nombre = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.IntegerField(default=0)

    @property
    def total(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.nombre} x{self.cantidad} - Total: ${self.total}"
    



# Create your models here.
