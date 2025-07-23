#!/usr/bin/env python3
"""
Script completo para configurar la base de datos GanaderiaBi
Ejecuta todo el proceso de configuración de una vez
"""

import subprocess
import sys
from pathlib import Path


def run_script(script_name, description):
    """Ejecuta un script y muestra el resultado"""
    print(f"\n🔧 {description}...")
    print(f"📁 Ejecutando: {script_name}")

    try:
        result = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        if result.returncode == 0:
            print("✅ Ejecutado exitosamente")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error en la ejecución")
            if result.stderr:
                print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False

    return True


def test_connection():
    """Prueba la conexión final a la base de datos"""
    print("\n🧪 Probando conexión final...")

    try:
        result = subprocess.run(
            [sys.executable, "scripts/test_db_connection.py"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        if result.returncode == 0:
            print("✅ Conexión exitosa")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Error en la conexión")
            if result.stderr:
                print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False


def main():
    """Función principal"""
    print("🐄 Configurador Completo de Base de Datos GanaderiaBi")
    print("=" * 60)

    # Lista de scripts a ejecutar en orden
    scripts = [
        ("create_db_simple.py", "Creando base de datos y usuario"),
        ("create_tables.py", "Creando tablas"),
        ("insert_test_data_fixed.py", "Insertando datos de prueba"),
    ]

    # Ejecutar cada script
    for script_name, description in scripts:
        if not run_script(script_name, description):
            print(f"\n❌ Error en {script_name}. Deteniendo proceso.")
            return False

    # Probar conexión final
    if not test_connection():
        print("\n❌ Error en la conexión final.")
        return False

    print("\n🎉 ¡Configuración completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("   1. Ejecutar servidor: python manage.py runserver")
    print("   2. Crear superusuario: python manage.py createsuperuser")
    print("   3. Acceder al admin: http://localhost:8000/admin/")
    print("   4. Probar APIs: http://localhost:8000/api/analytics/")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
