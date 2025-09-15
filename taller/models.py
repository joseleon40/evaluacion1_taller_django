from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vehiculos")
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()

    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo} ({self.anio})"


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class OrdenReparacion(models.Model):
    ESTADO_INGRESADO = "ingresado"
    ESTADO_EN_PROCESO = "en_proceso"
    ESTADO_TERMINADO = "terminado"
    ESTADO_ENTREGADO = "entregado"

    ESTADOS = [
        (ESTADO_INGRESADO, "Ingresado"),
        (ESTADO_EN_PROCESO, "En proceso"),
        (ESTADO_TERMINADO, "Terminado"),
        (ESTADO_ENTREGADO, "Entregado"),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="ordenes")
    servicios = models.ManyToManyField(Servicio, related_name="ordenes")
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_INGRESADO)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def calcularTotal(self):
        """Calcula el total de la orden sumando los servicios"""
        total = sum(servicio.precio for servicio in self.servicios.all())
        self.monto_total = total
        self.save()

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo.patente} ({self.estado})"
