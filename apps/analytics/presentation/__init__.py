# apps/analytics/presentation/__init__.py
"""
Capa de presentación - APIs, serialización y admin interface

Esta capa contiene todas las interfaces de usuario:
- Controllers: APIs REST
- Serializers: Serialización de datos
- URLs: Configuración de rutas
- Admin: Interfaz administrativa de Django
"""

# Importar configuración del admin para que Django lo registre
from .admin import *
