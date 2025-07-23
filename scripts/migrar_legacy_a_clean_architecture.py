#!/usr/bin/env python3
"""
Script para migrar datos del legacy business_intelligence a la nueva arquitectura Clean Architecture
"""

import os
import sys
import django
from datetime import datetime
from decimal import Decimal

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.db import transaction
from django.utils import timezone

# Importar modelos legacy
try:
    from business_intelligence.models import (
        MarcaGanadoBovino as MarcaLegacy,
        LogoMarcaBovina as LogoLegacy,
        KPIGanadoBovino as KPILegacy,
        HistorialEstadoMarca as HistorialLegacy,
    )

    LEGACY_AVAILABLE = True
except ImportError:
    print("⚠️  No se encontró la app legacy business_intelligence")
    LEGACY_AVAILABLE = False

# Importar modelos de la nueva arquitectura
from apps.analytics.infrastructure.models import (
    MarcaGanadoBovinoModel,
    LogoMarcaBovinaModel,
    KPIGanadoBovinoModel,
    HistorialEstadoMarcaModel,
)
from apps.analytics.domain.enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
    ModeloIA,
    CalidadLogo,
)


class LegacyToCleanArchitectureMigrator:
    """Migrador de datos del legacy a Clean Architecture"""

    def __init__(self):
        self.stats = {
            "marcas_migradas": 0,
            "logos_migrados": 0,
            "kpis_migrados": 0,
            "historial_migrado": 0,
            "errores": 0,
        }

    def migrar_todos_los_datos(self):
        """Migra todos los datos del legacy a la nueva arquitectura"""
        print("🚀 Iniciando migración de datos del legacy a Clean Architecture...")

        if not LEGACY_AVAILABLE:
            print("❌ No se puede migrar: app legacy no disponible")
            return False

        try:
            with transaction.atomic():
                self.migrar_marcas()
                self.migrar_logos()
                self.migrar_kpis()
                self.migrar_historial()

                print(f"✅ Migración completada exitosamente!")
                print(f"📊 Estadísticas:")
                print(f"   - Marcas migradas: {self.stats['marcas_migradas']}")
                print(f"   - Logos migrados: {self.stats['logos_migrados']}")
                print(f"   - KPIs migrados: {self.stats['kpis_migrados']}")
                print(f"   - Historial migrado: {self.stats['historial_migrado']}")
                print(f"   - Errores: {self.stats['errores']}")

                return True

        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            return False

    def migrar_marcas(self):
        """Migra las marcas del legacy a la nueva arquitectura"""
        print("📋 Migrando marcas...")

        marcas_legacy = MarcaLegacy.objects.all()

        for marca_legacy in marcas_legacy:
            try:
                # Mapear campos del legacy a la nueva arquitectura
                marca_nueva = MarcaGanadoBovinoModel(
                    numero_marca=marca_legacy.numero_marca,
                    nombre_productor=marca_legacy.nombre_productor,
                    fecha_registro=marca_legacy.fecha_registro,
                    fecha_procesamiento=marca_legacy.fecha_procesamiento,
                    estado=marca_legacy.estado,
                    monto_certificacion=marca_legacy.monto_certificacion,
                    raza_bovino=marca_legacy.raza_bovino,
                    proposito_ganado=marca_legacy.proposito_ganado,
                    cantidad_cabezas=marca_legacy.cantidad_cabezas,
                    departamento=marca_legacy.departamento,
                    municipio=marca_legacy.municipio,
                    comunidad=marca_legacy.comunidad,
                    ci_productor=marca_legacy.ci_productor,
                    telefono_productor=marca_legacy.telefono_productor,
                    tiempo_procesamiento_horas=marca_legacy.tiempo_procesamiento_horas,
                    observaciones=marca_legacy.observaciones,
                    creado_por=marca_legacy.creado_por,
                    actualizado_en=marca_legacy.actualizado_en,
                )
                marca_nueva.save()
                self.stats["marcas_migradas"] += 1

            except Exception as e:
                print(f"⚠️  Error migrando marca {marca_legacy.numero_marca}: {e}")
                self.stats["errores"] += 1

    def migrar_logos(self):
        """Migra los logos del legacy a la nueva arquitectura"""
        print("🎨 Migrando logos...")

        logos_legacy = LogoLegacy.objects.all()

        for logo_legacy in logos_legacy:
            try:
                # Buscar la marca correspondiente en la nueva arquitectura
                marca_nueva = MarcaGanadoBovinoModel.objects.filter(
                    numero_marca=logo_legacy.marca.numero_marca
                ).first()

                if not marca_nueva:
                    print(f"⚠️  No se encontró marca para logo {logo_legacy.id}")
                    continue

                logo_nuevo = LogoMarcaBovinaModel(
                    marca=marca_nueva,
                    url_logo=logo_legacy.url_logo,
                    fecha_generacion=logo_legacy.fecha_generacion,
                    exito=logo_legacy.exito,
                    tiempo_generacion_segundos=logo_legacy.tiempo_generacion_segundos,
                    modelo_ia_usado=logo_legacy.modelo_ia_usado,
                    prompt_usado=logo_legacy.prompt_usado,
                    calidad_logo=logo_legacy.calidad_logo,
                )
                logo_nuevo.save()
                self.stats["logos_migrados"] += 1

            except Exception as e:
                print(f"⚠️  Error migrando logo {logo_legacy.id}: {e}")
                self.stats["errores"] += 1

    def migrar_kpis(self):
        """Migra los KPIs del legacy a la nueva arquitectura"""
        print("📊 Migrando KPIs...")

        kpis_legacy = KPILegacy.objects.all()

        for kpi_legacy in kpis_legacy:
            try:
                kpi_nuevo = KPIGanadoBovinoModel(
                    fecha=kpi_legacy.fecha,
                    marcas_registradas_mes=kpi_legacy.marcas_registradas_mes,
                    tiempo_promedio_procesamiento=kpi_legacy.tiempo_promedio_procesamiento,
                    porcentaje_aprobacion=kpi_legacy.porcentaje_aprobacion,
                    ingresos_mes=kpi_legacy.ingresos_mes,
                    total_cabezas_registradas=kpi_legacy.total_cabezas_registradas,
                    promedio_cabezas_por_marca=kpi_legacy.promedio_cabezas_por_marca,
                    marcas_carne=kpi_legacy.marcas_carne,
                    marcas_leche=kpi_legacy.marcas_leche,
                    marcas_doble_proposito=kpi_legacy.marcas_doble_proposito,
                    marcas_reproduccion=kpi_legacy.marcas_reproduccion,
                    marcas_santa_cruz=kpi_legacy.marcas_santa_cruz,
                    marcas_beni=kpi_legacy.marcas_beni,
                    marcas_la_paz=kpi_legacy.marcas_la_paz,
                    marcas_otros_departamentos=kpi_legacy.marcas_otros_departamentos,
                    tasa_exito_logos=kpi_legacy.tasa_exito_logos,
                    total_logos_generados=kpi_legacy.total_logos_generados,
                    tiempo_promedio_generacion_logos=kpi_legacy.tiempo_promedio_generacion_logos,
                )
                kpi_nuevo.save()
                self.stats["kpis_migrados"] += 1

            except Exception as e:
                print(f"⚠️  Error migrando KPI {kpi_legacy.id}: {e}")
                self.stats["errores"] += 1

    def migrar_historial(self):
        """Migra el historial del legacy a la nueva arquitectura"""
        print("📝 Migrando historial...")

        historial_legacy = HistorialLegacy.objects.all()

        for historial_legacy_item in historial_legacy:
            try:
                # Buscar la marca correspondiente en la nueva arquitectura
                marca_nueva = MarcaGanadoBovinoModel.objects.filter(
                    numero_marca=historial_legacy_item.marca.numero_marca
                ).first()

                if not marca_nueva:
                    print(
                        f"⚠️  No se encontró marca para historial {historial_legacy_item.id}"
                    )
                    continue

                historial_nuevo = HistorialEstadoMarcaModel(
                    marca=marca_nueva,
                    estado_anterior=historial_legacy_item.estado_anterior,
                    estado_nuevo=historial_legacy_item.estado_nuevo,
                    fecha_cambio=historial_legacy_item.fecha_cambio,
                    usuario_responsable=historial_legacy_item.usuario_responsable,
                    observaciones_cambio=historial_legacy_item.observaciones_cambio,
                )
                historial_nuevo.save()
                self.stats["historial_migrado"] += 1

            except Exception as e:
                print(f"⚠️  Error migrando historial {historial_legacy_item.id}: {e}")
                self.stats["errores"] += 1

    def verificar_migracion(self):
        """Verifica que la migración fue exitosa"""
        print("🔍 Verificando migración...")

        # Contar registros en ambas arquitecturas
        if LEGACY_AVAILABLE:
            marcas_legacy_count = MarcaLegacy.objects.count()
            logos_legacy_count = LogoLegacy.objects.count()
            kpis_legacy_count = KPILegacy.objects.count()
            historial_legacy_count = HistorialLegacy.objects.count()
        else:
            marcas_legacy_count = logos_legacy_count = kpis_legacy_count = (
                historial_legacy_count
            ) = 0

        marcas_nuevas_count = MarcaGanadoBovinoModel.objects.count()
        logos_nuevos_count = LogoMarcaBovinaModel.objects.count()
        kpis_nuevos_count = KPIGanadoBovinoModel.objects.count()
        historial_nuevo_count = HistorialEstadoMarcaModel.objects.count()

        print(f"📊 Comparación de registros:")
        print(f"   Marcas: Legacy={marcas_legacy_count} → Nueva={marcas_nuevas_count}")
        print(f"   Logos: Legacy={logos_legacy_count} → Nueva={logos_nuevos_count}")
        print(f"   KPIs: Legacy={kpis_legacy_count} → Nueva={kpis_nuevos_count}")
        print(
            f"   Historial: Legacy={historial_legacy_count} → Nueva={historial_nuevo_count}"
        )

        # Verificar que los números coinciden
        if (
            marcas_legacy_count == marcas_nuevas_count
            and logos_legacy_count == logos_nuevos_count
            and kpis_legacy_count == kpis_nuevos_count
            and historial_legacy_count == historial_nuevo_count
        ):
            print("✅ Migración verificada exitosamente")
            return True
        else:
            print("⚠️  Algunos registros no coinciden")
            return False


def main():
    """Función principal del script"""
    print("🐄 Migrador de Legacy a Clean Architecture")
    print("=" * 50)

    migrator = LegacyToCleanArchitectureMigrator()

    # Ejecutar migración
    success = migrator.migrar_todos_los_datos()

    if success:
        # Verificar migración
        migrator.verificar_migracion()

        print("\n🎉 ¡Migración completada!")
        print("💡 Próximos pasos:")
        print("   1. Verificar que todo funciona correctamente")
        print("   2. Ejecutar tests para validar la nueva arquitectura")
        print("   3. Eliminar la app legacy cuando esté seguro")
    else:
        print("\n❌ La migración falló")
        sys.exit(1)


if __name__ == "__main__":
    main()
