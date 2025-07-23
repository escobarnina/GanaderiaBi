"""
Controllers de Clean Architecture para Historial de ganado bovino
Organizados por responsabilidad siguiendo principios SOLID
"""

# CRUD Controllers
from .crud_controller import (
    listar_historial,
    obtener_historial,
    historial_por_marca,
)

# Actividad Controllers
from .actividad_controller import (
    actividad_reciente,
    auditoria_usuario,
)

# Patrones Controllers
from .patrones_controller import (
    patrones_cambio_estado,
    analisis_flujos_estado,
)

# Eficiencia Controllers
from .eficiencia_controller import (
    eficiencia_evaluadores,
    evaluador_detalle,
    comparativa_evaluadores,
)

__all__ = [
    # CRUD
    "listar_historial",
    "obtener_historial",
    "historial_por_marca",
    # Actividad
    "actividad_reciente",
    "auditoria_usuario",
    # Patrones
    "patrones_cambio_estado",
    "analisis_flujos_estado",
    # Eficiencia
    "eficiencia_evaluadores",
    "evaluador_detalle",
    "comparativa_evaluadores",
]
