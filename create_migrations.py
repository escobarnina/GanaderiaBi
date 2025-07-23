#!/usr/bin/env python3
"""
Script para crear migraciones de Django sin cargar toda la aplicación
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.core.management import execute_from_command_line


def main():
    """Ejecuta makemigrations para apps.analytics"""
    print("🚀 Creando migraciones para apps.analytics...")

    # Simular comando makemigrations
    sys.argv = ["manage.py", "makemigrations", "apps.analytics"]

    try:
        execute_from_command_line(sys.argv)
        print("✅ Migraciones creadas exitosamente")
    except Exception as e:
        print(f"❌ Error creando migraciones: {e}")
        return False

    return True


if __name__ == "__main__":
    main()
