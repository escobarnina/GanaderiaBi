# apps/analytics/domain/entities/marca_ganado_bovino.py
"""
Entidad de dominio para marca de ganado bovino
Representa una solicitud de certificación de marca ganadera
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ..enums import EstadoMarca, RazaBovino, PropositoGanado, Departamento
from .historial_estado_marca import HistorialEstadoMarca


@dataclass
class MarcaGanadoBovino:
    """
    Entidad de dominio para marca de ganado bovino
    Representa una solicitud de certificación de marca ganadera
    """

    numero_marca: str
    nombre_productor: str
    fecha_registro: datetime
    estado: EstadoMarca = EstadoMarca.PENDIENTE
    monto_certificacion: Decimal = Decimal("0")

    # Campos específicos para ganado bovino
    raza_bovino: RazaBovino = RazaBovino.CRIOLLO
    proposito_ganado: PropositoGanado = PropositoGanado.CARNE
    cantidad_cabezas: int = 0

    # Ubicación geográfica
    departamento: Departamento = Departamento.SANTA_CRUZ
    municipio: str = ""
    comunidad: Optional[str] = None

    # Datos del propietario
    ci_productor: str = ""
    telefono_productor: Optional[str] = None

    # Métricas de procesamiento
    fecha_procesamiento: Optional[datetime] = None
    tiempo_procesamiento_horas: Optional[int] = None

    # Observaciones
    observaciones: Optional[str] = None

    # Metadatos
    creado_por: Optional[str] = None
    actualizado_en: Optional[datetime] = None

    # ID para persistencia (opcional)
    id: Optional[int] = None

    def __post_init__(self):
        """Validaciones de dominio"""
        if self.cantidad_cabezas < 1:
            raise ValueError("La cantidad de cabezas debe ser al menos 1")

        if self.monto_certificacion < 0:
            raise ValueError("El monto de certificación no puede ser negativo")

        if self.fecha_procesamiento and self.fecha_procesamiento < self.fecha_registro:
            raise ValueError(
                "La fecha de procesamiento no puede ser anterior al registro"
            )

    @property
    def esta_procesado(self) -> bool:
        """Retorna True si la marca ya fue procesada"""
        return self.estado in [EstadoMarca.APROBADO, EstadoMarca.RECHAZADO]

    @property
    def dias_desde_registro(self) -> int:
        """Retorna los días transcurridos desde el registro"""
        if self.fecha_registro:
            return (datetime.now().date() - self.fecha_registro.date()).days
        return 0

    def cambiar_estado(
        self, nuevo_estado: EstadoMarca, usuario: str = None
    ) -> HistorialEstadoMarca:
        """Cambia el estado de la marca y retorna el historial"""
        estado_anterior = self.estado
        self.estado = nuevo_estado

        return HistorialEstadoMarca(
            marca_id=self.id,
            estado_anterior=estado_anterior.value,
            estado_nuevo=nuevo_estado.value,
            usuario_responsable=usuario,
        )
