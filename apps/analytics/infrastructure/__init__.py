"""
Módulo de infraestructura para la aplicación de analytics.

Este módulo contiene las implementaciones concretas de la
capa de infraestructura, incluyendo repositorios y container.
"""

from .container import get_container, configure_container

__all__ = [
    "get_container",
    "configure_container",
]
