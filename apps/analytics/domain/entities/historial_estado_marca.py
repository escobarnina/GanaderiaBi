# apps/analytics/domain/entities/historial_estado_marca.py
"""
Entidad de dominio para historial de cambios de estado
Representa un registro de cambio de estado de una marca
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class HistorialEstadoMarca:
    """
    Entidad de dominio para historial de cambios de estado
    Representa un registro de cambio de estado de una marca
    """

    marca_id: int
    estado_nuevo: str
    estado_anterior: Optional[str] = None
    fecha_cambio: datetime = field(default_factory=datetime.now)
    usuario_responsable: Optional[str] = None
    observaciones_cambio: Optional[str] = None

    # ID para persistencia (opcional)
    id: Optional[int] = None

    def __post_init__(self):
        """Validaciones de dominio"""
        if not self.estado_nuevo:
            raise ValueError("El estado nuevo es requerido")
