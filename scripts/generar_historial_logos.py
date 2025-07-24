#!/usr/bin/env python
"""
Script para generar historial de logos de prueba
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ganaderia_bi.settings")
django.setup()

from apps.analytics.infrastructure.models import (
    LogoMarcaBovinaModel,
    MarcaGanadoBovinoModel,
)
from apps.analytics.domain.enums import ModeloIA, CalidadLogo
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType


def generar_historial_logos():
    """Genera historial de cambios para logos existentes"""
    print("🔄 Generando historial de logos...")

    # Obtener todos los logos existentes
    logos = LogoMarcaBovinaModel.objects.all()

    if not logos.exists():
        print("❌ No hay logos en la base de datos")
        return False

    print(f"📊 Encontrados {logos.count()} logos para procesar")

    for logo in logos:
        print(f"📝 Procesando logo {logo.pk}...")

        # Simular cambios en el logo para crear historial
        cambios_realizados = []

        # Cambio 1: Modificar calidad del logo
        if logo.calidad_logo == CalidadLogo.MEDIA.value:
            logo.calidad_logo = CalidadLogo.ALTA.value
            cambios_realizados.append("Calidad: MEDIA → ALTA")
        elif logo.calidad_logo == CalidadLogo.BAJA.value:
            logo.calidad_logo = CalidadLogo.MEDIA.value
            cambios_realizados.append("Calidad: BAJA → MEDIA")

        # Cambio 2: Modificar tiempo de generación
        tiempo_original = logo.tiempo_generacion_segundos
        nuevo_tiempo = max(10, tiempo_original - random.randint(5, 15))
        if nuevo_tiempo != tiempo_original:
            logo.tiempo_generacion_segundos = nuevo_tiempo
            cambios_realizados.append(f"Tiempo: {tiempo_original}s → {nuevo_tiempo}s")

        # Cambio 3: Modificar prompt si existe
        if logo.prompt_usado and len(logo.prompt_usado) > 20:
            prompt_original = logo.prompt_usado
            logo.prompt_usado = prompt_original + " [Mejorado]"
            cambios_realizados.append("Prompt actualizado")

        # Guardar cambios si se realizaron
        if cambios_realizados:
            logo.save()
            print(f"✅ Logo {logo.pk}: {len(cambios_realizados)} cambios registrados")
        else:
            print(f"ℹ️ Logo {logo.pk}: Sin cambios necesarios")

    print("✅ Historial de logos generado exitosamente")
    return True


def generar_historial_marcas():
    """Genera historial de cambios para marcas existentes"""
    print("🔄 Generando historial de marcas...")

    # Obtener todas las marcas existentes
    marcas = MarcaGanadoBovinoModel.objects.all()

    if not marcas.exists():
        print("❌ No hay marcas en la base de datos")
        return False

    print(f"📊 Encontradas {marcas.count()} marcas para procesar")

    for marca in marcas:
        print(f"📝 Procesando marca {marca.pk}...")

        # Simular cambios en la marca para crear historial
        cambios_realizados = []

        # Cambio 1: Modificar estado si está pendiente
        if marca.estado == "PENDIENTE":
            marca.estado = "EN_PROCESO"
            cambios_realizados.append("Estado: PENDIENTE → EN_PROCESO")

        # Cambio 2: Modificar observaciones
        if not marca.observaciones:
            marca.observaciones = "Revisión inicial completada"
            cambios_realizados.append("Observaciones actualizadas")

        # Cambio 3: Modificar monto de certificación
        if marca.monto_certificacion == 0:
            nuevo_monto = random.randint(1000, 5000)
            marca.monto_certificacion = nuevo_monto
            cambios_realizados.append(f"Monto: 0 → {nuevo_monto}")

        # Guardar cambios si se realizaron
        if cambios_realizados:
            marca.save()
            print(f"✅ Marca {marca.pk}: {len(cambios_realizados)} cambios registrados")
        else:
            print(f"ℹ️ Marca {marca.pk}: Sin cambios necesarios")

    print("✅ Historial de marcas generado exitosamente")
    return True


def mostrar_estadisticas_historial():
    """Muestra estadísticas del historial generado"""
    print("\n📊 Estadísticas del Historial:")

    # Estadísticas de logos
    content_type_logos = ContentType.objects.get_for_model(LogoMarcaBovinaModel)
    logs_logos = LogEntry.objects.filter(content_type=content_type_logos)

    print(f"📝 Logs de logos: {logs_logos.count()}")
    print(f"  - Creaciones: {logs_logos.filter(action_flag=ADDITION).count()}")
    print(f"  - Cambios: {logs_logos.filter(action_flag=CHANGE).count()}")

    # Estadísticas de marcas
    content_type_marcas = ContentType.objects.get_for_model(MarcaGanadoBovinoModel)
    logs_marcas = LogEntry.objects.filter(content_type=content_type_marcas)

    print(f"📝 Logs de marcas: {logs_marcas.count()}")
    print(f"  - Creaciones: {logs_marcas.filter(action_flag=ADDITION).count()}")
    print(f"  - Cambios: {logs_marcas.filter(action_flag=CHANGE).count()}")

    # Mostrar algunos ejemplos de cambios
    print("\n🔍 Ejemplos de cambios registrados:")
    cambios_recientes = LogEntry.objects.filter(action_flag=CHANGE).order_by(
        "-action_time"
    )[:5]
    for cambio in cambios_recientes:
        print(
            f"  - {cambio.action_time.strftime('%d/%m/%Y %H:%M')}: {cambio.change_message}"
        )


def main():
    """Función principal"""
    print("🚀 Iniciando generación de historial...")

    try:
        # Generar historial de logos
        if generar_historial_logos():
            print("✅ Historial de logos completado")
        else:
            print("❌ Error al generar historial de logos")

        # Generar historial de marcas
        if generar_historial_marcas():
            print("✅ Historial de marcas completado")
        else:
            print("❌ Error al generar historial de marcas")

        # Mostrar estadísticas
        mostrar_estadisticas_historial()

        print("\n🎉 Proceso completado exitosamente!")
        print("💡 Ahora puedes ver el historial en:")
        print(
            "   - http://localhost:8000/admin/analytics/logomarcabovinamodel/3/history/"
        )
        print(
            "   - http://localhost:8000/admin/analytics/marcaganadobovinomodel/1/history/"
        )

        return 0

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
