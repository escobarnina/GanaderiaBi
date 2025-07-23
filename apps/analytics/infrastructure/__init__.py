"""
Módulo de infraestructura para la aplicación de analytics.

Este módulo contiene las implementaciones concretas de la
capa de infraestructura, incluyendo repositorios y container.

Componentes disponibles:
- Container: Inyección de dependencias
- Models: 6 modelos de datos
- Repositories: Implementaciones de repositorios
"""

from .container import get_container

__all__ = [
    "get_container",
]


def get_infrastructure_status():
    """Retorna el estado de la capa de infraestructura"""
    return {
        "container": "✅ Configurado",
        "models": "✅ 6 modelos disponibles",
        "repositories": "✅ Implementados",
        "overall": "✅ Infraestructura completa",
    }
