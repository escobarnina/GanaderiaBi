#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del proyecto
"""
import os
import sys
import subprocess
import time
from pathlib import Path


def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        if result.returncode == 0:
            print("✅ Comando ejecutado exitosamente")
            if result.stdout:
                print("📄 Salida:")
                print(result.stdout)
        else:
            print("❌ Error en la ejecución")
            if result.stderr:
                print("📄 Error:")
                print(result.stderr)
            if result.stdout:
                print("📄 Salida:")
                print(result.stdout)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False


def main():
    """Función principal para ejecutar todos los tests"""
    print("🚀 Iniciando verificación completa del proyecto")
    print(f"📁 Directorio actual: {Path(__file__).parent.parent}")

    start_time = time.time()

    # Lista de verificaciones a realizar
    checks = [
        {
            "command": "python manage.py check",
            "description": "Verificando configuración de Django",
        },
        {
            "command": "python manage.py showmigrations apps.analytics",
            "description": "Verificando migraciones de la app analytics",
        },
        {
            "command": "python -m pytest tests/test_project_structure.py -v",
            "description": "Ejecutando tests de estructura del proyecto",
        },
        {
            "command": "python -m pytest tests/test_functionality.py -v",
            "description": "Ejecutando tests de funcionalidad básica",
        },
        {
            "command": "python -m pytest tests/test_integration.py -v",
            "description": "Ejecutando tests de integración",
        },
        {
            "command": "python -c \"from apps.analytics.infrastructure.container.main_container import Container; c = Container(); print('✅ Container inicializado correctamente')\"",
            "description": "Verificando inicialización del container",
        },
        {
            "command": "python -c \"from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino; from apps.analytics.domain.enums import EstadoMarca; m = MarcaGanadoBovino('TEST', 'Test', 'Test', 'Test', 100, EstadoMarca.PENDIENTE); print('✅ Entidad de dominio creada correctamente')\"",
            "description": "Verificando creación de entidades de dominio",
        },
        {
            "command": "python -c \"from apps.analytics.use_cases.marca.crear_marca_use_case import CrearMarcaUseCase; print('✅ Use case importado correctamente')\"",
            "description": "Verificando imports de use cases",
        },
        {
            "command": "python -c \"from apps.analytics.presentation.serializers.marca_serializers import MarcaSerializer; print('✅ Serializer importado correctamente')\"",
            "description": "Verificando imports de serializers",
        },
        {
            "command": "python -c \"from apps.analytics.presentation.controllers.marca.crud_controller import MarcaController; print('✅ Controller importado correctamente')\"",
            "description": "Verificando imports de controllers",
        },
    ]

    # Ejecutar verificaciones
    results = []
    for check in checks:
        success = run_command(check["command"], check["description"])
        results.append({"description": check["description"], "success": success})

    # Generar reporte final
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"\n{'='*60}")
    print("📊 REPORTE FINAL DE VERIFICACIÓN")
    print(f"{'='*60}")

    successful_checks = sum(1 for result in results if result["success"])
    total_checks = len(results)

    print(f"✅ Verificaciones exitosas: {successful_checks}/{total_checks}")
    print(f"⏱️  Tiempo total de ejecución: {execution_time:.2f} segundos")

    if successful_checks == total_checks:
        print("🎉 ¡TODAS LAS VERIFICACIONES EXITOSAS!")
        print("✅ El proyecto está funcionando correctamente")
    else:
        print("⚠️  Algunas verificaciones fallaron")
        print("📋 Verificaciones que fallaron:")
        for result in results:
            if not result["success"]:
                print(f"   ❌ {result['description']}")

    print(f"\n{'='*60}")
    print("📁 Archivos de test creados:")
    print("   - tests/test_project_structure.py")
    print("   - tests/test_functionality.py")
    print("   - tests/test_integration.py")
    print("   - tests/run_tests.py")
    print(f"{'='*60}")

    return successful_checks == total_checks


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
