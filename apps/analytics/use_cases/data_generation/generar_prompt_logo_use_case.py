"""
Use Case para generar prompts de logo usando IA
Responsabilidad única: Generar prompts específicos para logos de ganado bovino
"""

from typing import List

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)


class GenerarPromptLogoUseCase:
    """Use Case para generar prompts específicos para logos de ganado bovino"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> List[str]:
        """
        Genera prompts específicos para logos de ganado bovino usando IA

        Args:
            marca_id: ID de la marca

        Returns:
            List[str]: Lista de prompts generados

        Raises:
            ValueError: Si la marca no existe
        """
        # Obtener marca
        marca = self.marca_repository.obtener_por_id(marca_id)
        if not marca:
            raise ValueError(f"Marca con ID {marca_id} no encontrada")

        # Generar prompts
        prompts = self._generar_prompts_logo(marca)

        return prompts

    def _generar_prompts_logo(self, marca: MarcaGanadoBovino) -> List[str]:
        """
        Genera prompts específicos para logos

        Args:
            marca: Entidad de marca

        Returns:
            List[str]: Lista de prompts generados
        """
        prompts_templates = [
            self._generar_prompt_corporativo(marca),
            self._generar_prompt_rural(marca),
            self._generar_prompt_profesional(marca),
            self._generar_prompt_tradicional(marca),
        ]

        return [prompt for prompt in prompts_templates if prompt]

    def _generar_prompt_corporativo(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera prompt corporativo moderno

        Args:
            marca: Entidad de marca

        Returns:
            str: Prompt corporativo
        """
        return (
            f"Logo profesional para estancia ganadera {marca.nombre_productor}, "
            f"ganado {marca.raza_bovino.value}, {marca.proposito_ganado.value}, "
            f"estilo corporativo moderno, colores tierra"
        )

    def _generar_prompt_rural(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera prompt rural con elementos tradicionales

        Args:
            marca: Entidad de marca

        Returns:
            str: Prompt rural
        """
        return (
            f"Diseño de marca para {marca.cantidad_cabezas} cabezas de ganado bovino "
            f"raza {marca.raza_bovino.value}, elementos rurales, "
            f"{marca.departamento.value} Bolivia"
        )

    def _generar_prompt_profesional(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera prompt profesional con silueta de toro

        Args:
            marca: Entidad de marca

        Returns:
            str: Prompt profesional
        """
        return (
            f"Logo ganadero profesional, silueta de toro {marca.raza_bovino.value}, "
            f"marca {marca.numero_marca}, identidad visual robusta"
        )

    def _generar_prompt_tradicional(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera prompt tradicional boliviano

        Args:
            marca: Entidad de marca

        Returns:
            str: Prompt tradicional
        """
        return (
            f"Emblema para producción {marca.proposito_ganado.value} de ganado bovino, "
            f"{marca.municipio}, diseño tradicional boliviano contemporáneo"
        )
