from typing import Optional
from datetime import datetime

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
