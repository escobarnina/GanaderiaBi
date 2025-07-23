"""
Configuración del sitio administrativo para Clean Architecture.

Este archivo configura el sitio administrativo de Django
siguiendo los principios de Clean Architecture.
"""

from django.contrib import admin
from django.conf import settings


def configure_admin_site():
    """Configura el sitio administrativo con los valores de settings"""
    admin.site.site_header = getattr(
        settings,
        "ADMIN_SITE_HEADER",
        "🐄 Administración - Sistema de Marcas Ganaderas Bovinas (Clean Architecture)",
    )
    admin.site.site_title = getattr(settings, "ADMIN_SITE_TITLE", "Ganado Bovino Admin")
    admin.site.index_title = getattr(
        settings,
        "ADMIN_INDEX_TITLE",
        "Panel de Control - Inteligencia de Negocios Ganadera",
    )


# Configurar el sitio administrativo
configure_admin_site()
