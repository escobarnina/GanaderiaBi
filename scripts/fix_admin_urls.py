#!/usr/bin/env python3
"""
Script para solucionar el problema de URLs del admin.
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings


def fix_admin_urls():
    """Solucionar las URLs del admin."""

    print("🔧 Solucionando URLs del admin...")

    # Registrar las apps del admin manualmente
    try:
        from apps.analytics.presentation.admin import (
            MarcaGanadoBovinoAdmin,
            LogoMarcaBovinaAdmin,
            KPIGanadoBovinoAdmin,
            HistorialEstadoMarcaAdmin,
            DashboardDataAdmin,
            ReporteDataAdmin,
        )

        # Registrar los modelos en el admin
        from apps.analytics.infrastructure.models import (
            MarcaGanadoBovinoModel,
            LogoMarcaBovinaModel,
            KPIGanadoBovinoModel,
            HistorialEstadoMarcaModel,
            DashboardDataModel,
            ReporteDataModel,
        )

        admin.site.register(MarcaGanadoBovinoModel, MarcaGanadoBovinoAdmin)
        admin.site.register(LogoMarcaBovinaModel, LogoMarcaBovinaAdmin)
        admin.site.register(KPIGanadoBovinoModel, KPIGanadoBovinoAdmin)
        admin.site.register(HistorialEstadoMarcaModel, HistorialEstadoMarcaAdmin)
        admin.site.register(DashboardDataModel, DashboardDataAdmin)
        admin.site.register(ReporteDataModel, ReporteDataAdmin)

        print("✅ Modelos registrados en el admin")

    except Exception as e:
        print(f"❌ Error registrando modelos: {e}")

    # Verificar que las apps estén en INSTALLED_APPS
    if "apps.analytics" not in settings.INSTALLED_APPS:
        print("❌ App analytics no está en INSTALLED_APPS")
        return False

    print("✅ App analytics está en INSTALLED_APPS")

    # Verificar que las migraciones estén aplicadas
    try:
        from django.db import connection

        cursor = connection.cursor()

        # Verificar tabla de migraciones
        cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'analytics'")
        count = cursor.fetchone()[0]

        if count == 0:
            print("⚠️  No hay migraciones aplicadas para analytics")
            return False

        print(f"✅ {count} migraciones aplicadas para analytics")

    except Exception as e:
        print(f"❌ Error verificando migraciones: {e}")
        return False

    return True


if __name__ == "__main__":
    success = fix_admin_urls()
    if success:
        print("\n🎉 URLs del admin solucionadas correctamente")
    else:
        print("\n⚠️  Hay problemas que necesitan atención")
