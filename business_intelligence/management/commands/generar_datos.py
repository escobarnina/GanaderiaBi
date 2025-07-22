# business_intelligence/management/commands/generar_datos.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from business_intelligence.models import (
    MarcaGanadoBovino,
    LogoMarcaBovina,
    KPIGanadoBovino,
    HistorialEstadoMarca,
)
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = "Genera datos de prueba para el sistema de inteligencia de negocios de ganado bovino"

    def __init__(self):
        super().__init__()
        self.fake = Faker("es_MX")

    def add_arguments(self, parser):
        parser.add_argument(
            "--marcas", type=int, default=100, help="Número de marcas bovinas a generar"
        )
        parser.add_argument(
            "--logos", type=int, default=80, help="Número de logos a generar"
        )
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Limpiar datos existentes antes de generar nuevos",
        )

    def handle(self, *args, **options):
        if options["limpiar"]:
            self.stdout.write(self.style.WARNING("Limpiando datos existentes..."))
            MarcaGanadoBovino.objects.all().delete()
            LogoMarcaBovina.objects.all().delete()
            KPIGanadoBovino.objects.all().delete()
            HistorialEstadoMarca.objects.all().delete()

        self.generar_marcas_bovino(options["marcas"])
        self.generar_logos_bovinos(options["logos"])
        self.calcular_kpis_bovinos()

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Datos generados exitosamente: {options["marcas"]} marcas bovinas, {options["logos"]} logos'
            )
        )

    def generar_marcas_bovino(self, cantidad):
        """Genera marcas de ganado bovino con datos realistas"""

        # Departamentos y municipios de Bolivia con actividad ganadera
        ubicaciones = {
            "SANTA_CRUZ": [
                "Santa Cruz de la Sierra",
                "Montero",
                "Warnes",
                "La Guardia",
                "Cotoca",
                "Portachuelo",
                "Buena Vista",
                "San Javier",
            ],
            "BENI": [
                "Trinidad",
                "Riberalta",
                "Guayaramerín",
                "San Borja",
                "Reyes",
                "Santa Ana",
                "San Ignacio",
            ],
            "LA_PAZ": [
                "La Paz",
                "El Alto",
                "Viacha",
                "Achocalla",
                "Palca",
                "Coroico",
                "Caranavi",
            ],
            "COCHABAMBA": [
                "Cochabamba",
                "Quillacollo",
                "Sacaba",
                "Colcapirhua",
                "Tiquipaya",
                "Punata",
            ],
            "TARIJA": ["Tarija", "Yacuiba", "Villamontes", "Bermejo", "Padcaya"],
            "POTOSI": ["Potosí", "Uyuni", "Tupiza", "Villazón"],
            "ORURO": ["Oruro", "Challapata", "Huanuni"],
            "CHUQUISACA": ["Sucre", "Monteagudo", "Camargo"],
            "PANDO": ["Cobija", "Porvenir"],
        }

        # Razas bovinas comunes en Bolivia
        razas_bovinas = [
            "NELORE",
            "BRAHMAN",
            "CRIOLLO",
            "SANTA_GERTRUDIS",
            "CHAROLAIS",
            "GUZERAT",
            "MIXTO",
            "ANGUS",
            "HEREFORD",
        ]

        # Propósitos según la región
        propositos_por_region = {
            "SANTA_CRUZ": ["CARNE", "DOBLE_PROPOSITO"],
            "BENI": ["CARNE", "DOBLE_PROPOSITO"],
            "LA_PAZ": ["LECHE", "DOBLE_PROPOSITO"],
            "COCHABAMBA": ["LECHE", "DOBLE_PROPOSITO"],
            "TARIJA": ["CARNE", "DOBLE_PROPOSITO"],
            "POTOSI": ["CARNE", "DOBLE_PROPOSITO"],
            "ORURO": ["CARNE"],
            "CHUQUISACA": ["CARNE", "DOBLE_PROPOSITO"],
            "PANDO": ["CARNE"],
        }

        estados = ["PENDIENTE", "EN_PROCESO", "APROBADO", "RECHAZADO"]

        self.stdout.write(f"🐄 Generando {cantidad} marcas de ganado bovino...")

        for i in range(cantidad):
            # Seleccionar departamento con pesos realistas (Santa Cruz y Beni más ganaderos)
            departamento = random.choices(
                list(ubicaciones.keys()),
                weights=[
                    30,
                    25,
                    15,
                    10,
                    8,
                    5,
                    3,
                    2,
                    2,
                ],  # Santa Cruz y Beni tienen más peso
                k=1,
            )[0]

            municipio = random.choice(ubicaciones[departamento])

            # Fecha aleatoria en los últimos 2 años
            fecha_registro = self.fake.date_time_between(
                start_date="-2y", end_date="now", tzinfo=timezone.get_current_timezone()
            )

            estado = random.choices(
                estados, weights=[20, 10, 60, 10], k=1  # Más aprobadas que pendientes
            )[0]

            # Datos de procesamiento
            fecha_procesamiento = None
            tiempo_procesamiento = None
            if estado in ["APROBADO", "RECHAZADO"]:
                fecha_procesamiento = fecha_registro + timedelta(
                    hours=random.randint(1, 168),  # Hasta una semana
                    minutes=random.randint(0, 59),
                )
                tiempo_procesamiento = random.randint(1, 168)

            # Raza según la región (algunas razas son más comunes en ciertas regiones)
            if departamento in ["SANTA_CRUZ", "BENI"]:
                raza = random.choices(
                    ["NELORE", "BRAHMAN", "CRIOLLO", "SANTA_GERTRUDIS", "GUZERAT"],
                    weights=[30, 25, 20, 15, 10],
                    k=1,
                )[0]
            else:
                raza = random.choices(
                    ["CRIOLLO", "HOLSTEIN", "MIXTO", "CHAROLAIS"],
                    weights=[40, 25, 20, 15],
                    k=1,
                )[0]

            # Propósito según región
            proposito = random.choice(
                propositos_por_region.get(departamento, ["CARNE"])
            )

            # Cantidad de cabezas realista según el propósito
            if proposito == "LECHE":
                cantidad_cabezas = random.randint(5, 80)
            elif proposito == "CARNE":
                cantidad_cabezas = random.randint(10, 500)
            elif proposito == "DOBLE_PROPOSITO":
                cantidad_cabezas = random.randint(8, 200)
            else:  # REPRODUCCION
                cantidad_cabezas = random.randint(3, 50)

            # Monto según cantidad de cabezas y propósito
            monto_base = {
                "LECHE": 15,
                "CARNE": 12,
                "DOBLE_PROPOSITO": 10,
                "REPRODUCCION": 20,
            }

            monto_por_cabeza = monto_base[proposito]
            monto_total = Decimal(
                str(monto_por_cabeza * cantidad_cabezas + random.uniform(50, 200))
            ).quantize(Decimal("0.01"))

            # Generar datos del productor
            nombre_productor = self.fake.name()
            ci_productor = f"{random.randint(1000000, 9999999)}{random.choice(['LP', 'SC', 'CB', 'PT', 'OR', 'CH', 'TJ', 'BN', 'PD'])}"
            telefono_productor = (
                f"{random.choice([7, 6])}{random.randint(1000000, 9999999)}"
            )

            # Crear la marca
            marca = MarcaGanadoBovino.objects.create(
                numero_marca=f"MB-{i+1:06d}",
                nombre_productor=nombre_productor,
                fecha_registro=fecha_registro,
                fecha_procesamiento=fecha_procesamiento,
                estado=estado,
                monto_certificacion=monto_total,
                raza_bovino=raza,
                proposito_ganado=proposito,
                cantidad_cabezas=cantidad_cabezas,
                departamento=departamento,
                municipio=municipio,
                comunidad=self.fake.city() if random.random() < 0.3 else None,
                ci_productor=ci_productor,
                telefono_productor=telefono_productor,
                tiempo_procesamiento_horas=tiempo_procesamiento,
                observaciones=(
                    self.fake.text(max_nb_chars=200) if random.random() < 0.2 else None
                ),
                creado_por=f"admin_{random.randint(1, 5)}",
            )

            # Crear historial inicial
            HistorialEstadoMarca.objects.create(
                marca=marca,
                estado_anterior=None,
                estado_nuevo="PENDIENTE",
                usuario_responsable=f"sistema",
                observaciones_cambio=f"Registro inicial de marca {marca.numero_marca}",
            )

            # Si cambió de estado, crear registro adicional
            if estado != "PENDIENTE":
                HistorialEstadoMarca.objects.create(
                    marca=marca,
                    estado_anterior="PENDIENTE",
                    estado_nuevo=estado,
                    fecha_cambio=fecha_procesamiento or timezone.now(),
                    usuario_responsable=f"evaluador_{random.randint(1, 3)}",
                    observaciones_cambio=f"Marca {estado.lower()} después de evaluación",
                )

            if (i + 1) % 25 == 0:
                self.stdout.write(f"  📊 Generadas {i + 1} marcas bovinas...")

    def generar_logos_bovinos(self, cantidad):
        """Genera logos para marcas bovinas"""

        marcas_disponibles = list(MarcaGanadoBovino.objects.all())
        modelos_ia = [
            "GPT-4",
            "DALL-E-3",
            "DALL-E-2",
            "MIDJOURNEY",
            "STABLE_DIFFUSION",
            "LEONARDO_AI",
        ]

        calidades = ["ALTA", "MEDIA", "BAJA"]

        if not marcas_disponibles:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️ No hay marcas bovinas disponibles para generar logos"
                )
            )
            return

        self.stdout.write(f"🎨 Generando {cantidad} logos para marcas bovinas...")

        # Seleccionar marcas únicas para logos (evitar duplicados)
        marcas_seleccionadas = random.sample(
            marcas_disponibles, min(cantidad, len(marcas_disponibles))
        )

        for i, marca in enumerate(marcas_seleccionadas):
            # Fecha de generación después del registro
            fecha_generacion = marca.fecha_registro + timedelta(
                days=random.randint(0, 60), hours=random.randint(0, 23)
            )

            # Probabilidad de éxito según el modelo
            modelo = random.choice(modelos_ia)
            probabilidades_exito = {
                "GPT-4": 0.75,
                "DALL-E-3": 0.90,
                "DALL-E-2": 0.85,
                "MIDJOURNEY": 0.88,
                "STABLE_DIFFUSION": 0.80,
                "LEONARDO_AI": 0.82,
            }

            exito = random.random() < probabilidades_exito.get(modelo, 0.85)

            # Tiempo de generación según el modelo
            tiempos_base = {
                "GPT-4": (15, 45),
                "DALL-E-3": (20, 60),
                "DALL-E-2": (15, 40),
                "MIDJOURNEY": (30, 90),
                "STABLE_DIFFUSION": (10, 30),
                "LEONARDO_AI": (15, 45),
            }

            tiempo_min, tiempo_max = tiempos_base[modelo]
            tiempo_generacion = random.randint(tiempo_min, tiempo_max)

            # Calidad del logo (mejor calidad si fue exitoso)
            if exito:
                calidad = random.choices(
                    calidades,
                    weights=[40, 50, 10],  # Más probabilidad de alta/media calidad
                    k=1,
                )[0]
            else:
                calidad = "BAJA"

            # Generar prompt realista
            prompts_base = [
                f"Logo profesional para marca de ganado bovino {marca.numero_marca}, raza {marca.get_raza_bovino_display()}, estilo moderno",
                f"Diseño de marca ganadera para {marca.get_proposito_ganado_display()}, elementos bovinos, {marca.departamento}",
                f"Logo corporativo ganadería {marca.nombre_productor}, ganado {marca.get_raza_bovino_display()}, identidad visual",
                f"Marca registrada ganado bovino, símbolo {marca.get_proposito_ganado_display()}, diseño profesional",
            ]

            prompt_usado = random.choice(prompts_base)

            LogoMarcaBovina.objects.create(
                marca=marca,
                url_logo=f"https://logos.ganaderia.bo/bovino/{marca.numero_marca}_{modelo.lower().replace('-', '_')}.png",
                fecha_generacion=fecha_generacion,
                exito=exito,
                tiempo_generacion_segundos=tiempo_generacion,
                modelo_ia_usado=modelo,
                prompt_usado=prompt_usado,
                calidad_logo=calidad,
            )

            if (i + 1) % 10 == 0:
                self.stdout.write(f"  🎨 Generados {i + 1} logos...")

    def calcular_kpis_bovinos(self):
        """Calcula y guarda snapshots de KPIs específicos para ganado bovino"""

        self.stdout.write("📊 Calculando KPIs históricos para ganado bovino...")

        primera_marca = MarcaGanadoBovino.objects.order_by("fecha_registro").first()
        if not primera_marca:
            self.stdout.write(
                self.style.WARNING("⚠️ No hay marcas bovinas para calcular KPIs")
            )
            return

        fecha_inicio = primera_marca.fecha_registro.date()
        fecha_fin = timezone.now().date()

        # Generar KPIs por mes
        fecha_actual = fecha_inicio.replace(day=1)

        while fecha_actual <= fecha_fin:
            # Calcular siguiente mes
            if fecha_actual.month == 12:
                siguiente_mes = fecha_actual.replace(
                    year=fecha_actual.year + 1, month=1
                )
            else:
                siguiente_mes = fecha_actual.replace(month=fecha_actual.month + 1)

            # Filtro base para el mes
            marcas_mes = MarcaGanadoBovino.objects.filter(
                fecha_registro__date__gte=fecha_actual,
                fecha_registro__date__lt=siguiente_mes,
            )

            # KPIs principales
            total_marcas_mes = marcas_mes.count()

            # Total de cabezas registradas
            total_cabezas = (
                marcas_mes.aggregate(total=models.Sum("cantidad_cabezas"))["total"] or 0
            )

            # Promedio de cabezas por marca
            promedio_cabezas = (
                (total_cabezas / total_marcas_mes) if total_marcas_mes > 0 else 0
            )

            # Tiempo promedio de procesamiento
            tiempo_promedio = (
                marcas_mes.filter(tiempo_procesamiento_horas__isnull=False).aggregate(
                    promedio=models.Avg("tiempo_procesamiento_horas")
                )["promedio"]
                or 0
            )

            # Porcentaje de aprobación
            marcas_procesadas = marcas_mes.filter(estado__in=["APROBADO", "RECHAZADO"])
            total_procesadas = marcas_procesadas.count()
            aprobadas = marcas_procesadas.filter(estado="APROBADO").count()
            porcentaje_aprobacion = (
                (aprobadas / total_procesadas * 100) if total_procesadas > 0 else 0
            )

            # Ingresos del mes
            ingresos = (
                marcas_mes.filter(estado="APROBADO").aggregate(
                    total=models.Sum("monto_certificacion")
                )["total"]
                or 0
            )

            # Distribución por propósito
            marcas_carne = marcas_mes.filter(proposito_ganado="CARNE").count()
            marcas_leche = marcas_mes.filter(proposito_ganado="LECHE").count()
            marcas_doble = marcas_mes.filter(proposito_ganado="DOBLE_PROPOSITO").count()
            marcas_repro = marcas_mes.filter(proposito_ganado="REPRODUCCION").count()

            # Distribución geográfica
            marcas_sc = marcas_mes.filter(departamento="SANTA_CRUZ").count()
            marcas_beni = marcas_mes.filter(departamento="BENI").count()
            marcas_lp = marcas_mes.filter(departamento="LA_PAZ").count()
            marcas_otros = marcas_mes.exclude(
                departamento__in=["SANTA_CRUZ", "BENI", "LA_PAZ"]
            ).count()

            # KPIs de logos
            logos_mes = LogoMarcaBovina.objects.filter(
                fecha_generacion__date__gte=fecha_actual,
                fecha_generacion__date__lt=siguiente_mes,
            )

            total_logos = logos_mes.count()
            logos_exitosos = logos_mes.filter(exito=True).count()
            tasa_exito_logos = (
                (logos_exitosos / total_logos * 100) if total_logos > 0 else 0
            )

            tiempo_promedio_logos = (
                logos_mes.aggregate(promedio=models.Avg("tiempo_generacion_segundos"))[
                    "promedio"
                ]
                or 0
            )

            # Crear o actualizar KPI snapshot
            KPIGanadoBovino.objects.update_or_create(
                fecha=fecha_actual,
                defaults={
                    "marcas_registradas_mes": total_marcas_mes,
                    "tiempo_promedio_procesamiento": tiempo_promedio,
                    "porcentaje_aprobacion": porcentaje_aprobacion,
                    "ingresos_mes": ingresos,
                    "total_cabezas_registradas": total_cabezas,
                    "promedio_cabezas_por_marca": promedio_cabezas,
                    "marcas_carne": marcas_carne,
                    "marcas_leche": marcas_leche,
                    "marcas_doble_proposito": marcas_doble,
                    "marcas_reproduccion": marcas_repro,
                    "marcas_santa_cruz": marcas_sc,
                    "marcas_beni": marcas_beni,
                    "marcas_la_paz": marcas_lp,
                    "marcas_otros_departamentos": marcas_otros,
                    "tasa_exito_logos": tasa_exito_logos,
                    "total_logos_generados": total_logos,
                    "tiempo_promedio_generacion_logos": tiempo_promedio_logos,
                },
            )

            fecha_actual = siguiente_mes

        self.stdout.write(self.style.SUCCESS("✅ KPIs calculados exitosamente"))
