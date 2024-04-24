from django.db import models

# Create your models here.
class Clientes(models.Model):
    nombre=models.CharField(max_length=30)
    direccion=models.CharField(max_length=50, verbose_name="La direccion")
    email=models.EmailField(blank=True, null=True)
    tfno=models.CharField(max_length=7)

    def __str__(self):
        return self.nombre

class Articulos(models.Model):
    nombre=models.CharField(max_length=30)
    seccion=models.CharField(max_length=20)
    precio=models.IntegerField()
    

class Pedidos(models.Model):
    numero=models.IntegerField()
    fecha=models.DateField()
    entregado=models.BooleanField()

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()

class Implemento(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    edificio = models.CharField(max_length=100)
    disponibilidad = models.BooleanField(default=True)
    hora_reserva = models.TimeField(null=True, blank=True)
    hora_devolucion = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    