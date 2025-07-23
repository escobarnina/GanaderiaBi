"""
Controllers de Clean Architecture para marcas de ganado bovino
Organizados por responsabilidad siguiendo principios SOLID
"""

# CRUD Controllers
from .crud_controller import (
    listar_marcas,
    obtener_marca,
    crear_marca,
    actualizar_marca,
    eliminar_marca,
)

# Estado Controllers
from .estado_controller import (
    aprobar_marca,
    rechazar_marca,
)

# Consulta Controllers
from .consulta_controller import (
    marcas_pendientes,
    marcas_por_procesar,
    marcas_procesadas_hoy,
)

# Estadísticas Controllers
from .estadisticas_controller import (
    estadisticas_por_raza,
    estadisticas_por_departamento,
)

# Procesamiento Controllers
from .procesamiento_controller import (
    procesamiento_masivo,
)

__all__ = [
    # CRUD
    "listar_marcas",
    "obtener_marca",
    "crear_marca",
    "actualizar_marca",
    "eliminar_marca",
    # Estado
    "aprobar_marca",
    "rechazar_marca",
    # Consulta
    "marcas_pendientes",
    "marcas_por_procesar",
    "marcas_procesadas_hoy",
    # Estadísticas
    "estadisticas_por_raza",
    "estadisticas_por_departamento",
    # Procesamiento
    "procesamiento_masivo",
]
