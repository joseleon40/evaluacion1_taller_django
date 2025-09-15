import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evaluacion_1.settings") 
django.setup()

from taller.models import Cliente, Vehiculo, Servicio, OrdenReparacion

with open("shell_tests.txt", "w", encoding="utf-8") as f:

    #Vehículos de un cliente
    f.write("===== VEHÍCULOS DE UN CLIENTE =====\n")
    cliente = Cliente.objects.first()
    if cliente:
        f.write(f"Cliente: {cliente.nombre} {cliente.apellido}\n")
        for v in cliente.vehiculos.all():
            f.write(f"- {v.patente} - {v.marca} {v.modelo} ({v.anio})\n")
    else:
        f.write("No hay clientes registrados.\n")
    f.write("\n")

    #Órdenes de un vehículo
    f.write("===== ÓRDENES DE UN VEHÍCULO =====\n")
    vehiculo = Vehiculo.objects.first()
    if vehiculo:
        f.write(f"Vehículo: {vehiculo.patente} - {vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio})\n")
        for o in vehiculo.ordenes.all():
            f.write(f"- Orden #{o.id} ({o.estado})\n")
    else:
        f.write("No hay vehículos registrados.\n")
    f.write("\n")

    #Servicios asociados a una orden
    f.write("===== SERVICIOS DE UNA ORDEN =====\n")
    orden = OrdenReparacion.objects.first()
    if orden:
        f.write(f"Orden #{orden.id} - Vehículo: {orden.vehiculo.patente} ({orden.estado})\n")
        for s in orden.servicios.all():
            f.write(f"- {s.nombre} - ${s.precio:.2f}\n")
    else:
        f.write("No hay órdenes registradas.\n")
    f.write("\n")

    #Órdenes en progreso
    f.write("===== ÓRDENES EN PROGRESO ======\n")
    ordenes_progreso = OrdenReparacion.objects.filter(estado="en_proceso")
    if ordenes_progreso.exists():
        for o in ordenes_progreso:
            f.write(f"- Orden #{o.id} - Vehículo: {o.vehiculo.patente} | Cliente: {o.vehiculo.cliente.nombre} {o.vehiculo.cliente.apellido}\n")
    else:
        f.write("No hay órdenes en progreso.\n")
    f.write("\n")

    #Órdenes sin fecha_salida
    f.write("==== ÓRDENES SIN FECHA DE SALIDA ===\n")
    ordenes_sin_salida = OrdenReparacion.objects.filter(fecha_salida__isnull=True)
    if ordenes_sin_salida.exists():
        for o in ordenes_sin_salida:
            f.write(f"- Orden #{o.id} - Vehículo: {o.vehiculo.patente} | Cliente: {o.vehiculo.cliente.nombre} {o.vehiculo.cliente.apellido}\n")
    else:
        f.write("No hay órdenes sin fecha de salida.\n")

print("Resultados guardados en shell_tests.txt")
