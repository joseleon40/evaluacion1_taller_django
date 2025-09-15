from django.contrib import admin
from .models import Cliente, Vehiculo, Servicio, OrdenReparacion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "telefono", "correo")
    search_fields = ("nombre", "apellido", "telefono", "correo")


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("patente", "marca", "modelo", "anio", "cliente")
    search_fields = ("patente", "marca", "modelo")
    list_filter = ("marca", "anio")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    search_fields = ("nombre",)


@admin.register(OrdenReparacion)
class OrdenReparacionAdmin(admin.ModelAdmin):
    list_display = ("id", "vehiculo", "estado", "fecha_ingreso", "fecha_salida", "monto_total")
    list_filter = ("estado",)
    search_fields = ("vehiculo__patente",)
