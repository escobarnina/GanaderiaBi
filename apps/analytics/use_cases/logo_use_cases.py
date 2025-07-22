# apps/analytics/use_cases/logo_use_cases.py
"""
Use Cases para gestión de logos de marcas bovinas
Responsabilidad: Orquestar operaciones de negocio relacionadas con logos IA
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

from apps.analytics.domain.entities.logo_marca_bovina import LogoMarcaBovina
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import ModeloIA, CalidadLogo


class GenerarLogoUseCase:
    """Use Case para generar un logo usando IA"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(
        self,
        marca_id: int,
        modelo_ia: ModeloIA,
        prompt: str,
        usuario: Optional[str] = None,
    ) -> LogoMarcaBovina:
        """
        Genera un logo para una marca usando IA

        Args:
            marca_id: ID de la marca
            modelo_ia: Modelo de IA a usar
            prompt: Prompt para generar el logo
            usuario: Usuario que solicita la generación

        Returns:
            LogoMarcaBovina: El logo generado

        Raises:
            ValueError: Si los datos son inválidos
        """
        if not prompt:
            raise ValueError("El prompt es requerido para generar el logo")

        # Simular generación de logo (en producción se conectaría con servicio de IA)
        tiempo_generacion = 30  # segundos simulados
        exito = True  # Simular éxito
        url_logo = f"https://storage.example.com/logos/{marca_id}_{datetime.now().timestamp()}.png"

        # Crear entidad de dominio
        logo = LogoMarcaBovina(
            marca_id=marca_id,
            url_logo=url_logo,
            exito=exito,
            tiempo_generacion_segundos=tiempo_generacion,
            modelo_ia_usado=modelo_ia,
            prompt_usado=prompt,
            calidad_logo=CalidadLogo.MEDIA,  # Calidad por defecto
        )

        # Guardar usando repositorio
        return self.logo_repository.crear(logo)


class ObtenerLogoUseCase:
    """Use Case para obtener un logo por ID"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(self, logo_id: int) -> Optional[LogoMarcaBovina]:
        """
        Obtiene un logo por su ID

        Args:
            logo_id: ID del logo

        Returns:
            LogoMarcaBovina: El logo encontrado o None
        """
        return self.logo_repository.obtener_por_id(logo_id)


class ListarLogosUseCase:
    """Use Case para listar logos con filtros"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(
        self,
        marca_id: Optional[int] = None,
        modelo_ia: Optional[ModeloIA] = None,
        exito: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LogoMarcaBovina]:
        """
        Lista logos con filtros opcionales

        Args:
            marca_id: Filtrar por marca
            modelo_ia: Filtrar por modelo de IA
            exito: Filtrar por éxito de generación
            limit: Límite de resultados
            offset: Desplazamiento para paginación

        Returns:
            List[LogoMarcaBovina]: Lista de logos
        """
        return self.logo_repository.listar_con_filtros(
            marca_id=marca_id,
            modelo_ia=modelo_ia,
            exito=exito,
            limit=limit,
            offset=offset,
        )


class ObtenerEstadisticasLogosUseCase:
    """Use Case para obtener estadísticas de logos"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de logos generados

        Returns:
            Dict[str, Any]: Estadísticas de logos
        """
        return self.logo_repository.obtener_estadisticas()
