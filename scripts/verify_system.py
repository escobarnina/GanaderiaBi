#!/usr/bin/env python3
"""
Script para verificar que todo el sistema GanaderiaBi esté funcionando correctamente.
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

import mysql.connector
from mysql.connector import Error
import requests
import time


def verify_database():
    """Verificar la conexión y tablas de la base de datos."""
    print("🔍 Verificando base de datos...")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="bi_user",
            password="password",
            database="ganaderia_bi",
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Verificar tablas principales
            tables_to_check = [
                "auth_user",
                "django_content_type",
                "django_admin_log",
                "django_session",
                "django_migrations",
                "marca_ganado_bovino",
                "logo_marca_bovina",
                "kpi_ganado_bovino",
                "historial_estado_marca",
                "dashboard_data",
                "reporte_data",
            ]

            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Tabla {table}: {count} registros")
                except Error as e:
                    print(f"❌ Error en tabla {table}: {e}")

            # Verificar superusuario
            cursor.execute(
                "SELECT username, is_superuser FROM auth_user WHERE username = 'admin'"
            )
            user = cursor.fetchone()
            if user:
                print(f"✅ Superusuario {user[0]} existe (superuser: {user[1]})")
            else:
                print("❌ Superusuario admin no encontrado")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"❌ Error de conexión a BD: {e}")
        return False


def verify_django_apps():
    """Verificar que las apps de Django estén configuradas correctamente."""
    print("\n🔍 Verificando apps de Django...")

    try:
        from django.apps import apps
        from django.conf import settings

        # Verificar apps instaladas
        installed_apps = settings.INSTALLED_APPS
        print(f"✅ Apps instaladas: {len(installed_apps)}")

        # Verificar app analytics
        if "apps.analytics" in installed_apps:
            print("✅ App analytics instalada")
        else:
            print("❌ App analytics no encontrada")

        # Verificar modelos
        from apps.analytics.infrastructure.models import (
            MarcaGanadoBovinoModel,
            LogoMarcaBovinaModel,
            KPIGanadoBovinoModel,
        )

        print("✅ Modelos de analytics cargados correctamente")

        return True

    except Exception as e:
        print(f"❌ Error verificando apps: {e}")
        return False


def verify_server():
    """Verificar que el servidor esté funcionando."""
    print("\n🔍 Verificando servidor...")

    try:
        # Esperar un poco para que el servidor se inicie
        time.sleep(2)

        # Probar conexión al servidor
        response = requests.get("http://localhost:8000/admin/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor funcionando en http://localhost:8000")
            return True
        else:
            print(f"⚠️  Servidor responde con código: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error verificando servidor: {e}")
        return False


def main():
    """Función principal de verificación."""
    print("🐄 Verificación Completa del Sistema GanaderiaBi")
    print("=" * 60)

    # Verificaciones
    db_ok = verify_database()
    django_ok = verify_django_apps()
    server_ok = verify_server()

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN:")
    print(f"📁 Base de datos: {'✅ OK' if db_ok else '❌ ERROR'}")
    print(f"🐍 Django apps: {'✅ OK' if django_ok else '❌ ERROR'}")
    print(f"🌐 Servidor: {'✅ OK' if server_ok else '❌ ERROR'}")

    if db_ok and django_ok and server_ok:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\n📋 ACCESO AL SISTEMA:")
        print("🌐 Admin: http://localhost:8000/admin/")
        print("👤 Usuario: admin")
        print("🔑 Contraseña: admin123")
        print("📚 APIs: http://localhost:8000/api/docs/")
    else:
        print("\n⚠️  Hay problemas que necesitan atención")
        print("💡 Ejecuta los scripts de configuración nuevamente")


if __name__ == "__main__":
    main()
