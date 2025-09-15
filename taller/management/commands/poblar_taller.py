from django.core.management.base import BaseCommand
from taller.models import Servicio, Cliente, Vehiculo, OrdenReparacion
from faker import Faker
import random

class Command(BaseCommand):
    help = "Poblar la base de datos del taller con datos falsos"

    def handle(self, *args, **kwargs):
        fake = Faker("es_ES")

        self.stdout.write(self.style.WARNING("Eliminando datos previos..."))
        OrdenReparacion.objects.all().delete()
        Vehiculo.objects.all().delete()
        Cliente.objects.all().delete()
        Servicio.objects.all().delete()

        # Crear servicios base
        servicios = [
            Servicio.objects.create(nombre="Cambio de aceite", precio=25000),
            Servicio.objects.create(nombre="Revisión de frenos", precio=30000),
            Servicio.objects.create(nombre="Alineación y balanceo", precio=20000),
        ]
        self.stdout.write(self.style.SUCCESS(f"Servicios creados: {len(servicios)}"))

        # Crear clientes, vehículos y órdenes
        for _ in range(5):
            cliente = Cliente.objects.create(
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                correo=fake.email(),
                telefono=fake.phone_number(),
            )

            vehiculo = Vehiculo.objects.create(
                cliente=cliente,
                patente=fake.license_plate(),
                marca=fake.company(),
                modelo=fake.word().capitalize(),
                anio=fake.year(),
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Cliente y vehículo creados: {cliente.nombre} {cliente.apellido} / {vehiculo.patente} - {vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio})"
                )
            )

            # Crear orden de reparación
            orden = OrdenReparacion.objects.create(
                vehiculo=vehiculo,
                fecha_ingreso=fake.date_this_year(),
                estado=OrdenReparacion.ESTADO_INGRESADO,
            )

            # Agregar servicios aleatorios a la orden
            servicios_seleccionados = random.sample(servicios, random.randint(1, len(servicios)))
            orden.servicios.set(servicios_seleccionados)

            # Calcular monto total con tu método actual
            orden.calcularTotal()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Orden creada para {vehiculo.patente} con {len(servicios_seleccionados)} servicios."
                )
            )

        self.stdout.write(self.style.SUCCESS("Población de datos completada ✅"))

