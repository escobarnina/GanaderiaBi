"""
Use Case para generar descripción de marca usando LLM
Responsabilidad única: Generar descripciones personalizadas usando IA
"""

import requests
from typing import Optional
from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)


class GenerarDescripcionMarcaUseCase:
    """Use Case para generar descripción de marca usando LLM"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> str:
        """
        Genera descripción de marca usando LLM

        Args:
            marca_id: ID de la marca

        Returns:
            str: Descripción generada

        Raises:
            ValueError: Si la marca no existe
        """
        # Obtener marca
        marca = self.marca_repository.obtener_por_id(marca_id)
        if not marca:
            raise ValueError(f"Marca con ID {marca_id} no encontrada")

        # Generar descripción usando LLM
        descripcion = self._generar_descripcion_llm(marca)

        return descripcion

    def _generar_descripcion_llm(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera descripción usando LLM

        Args:
            marca: Entidad de marca

        Returns:
            str: Descripción generada
        """
        try:
            # Crear prompt para el LLM
            prompt = self._crear_prompt_descripcion(marca)

            # En un entorno real, aquí se haría la llamada al LLM
            # Por ahora, simulamos la generación
            descripcion = self._simular_generacion_llm(prompt, marca)

            return descripcion
        except Exception as e:
            print(f"Error generando descripción con LLM: {e}")
            return self._generar_descripcion_fallback(marca)

    def _crear_prompt_descripcion(self, marca: MarcaGanadoBovino) -> str:
        """
        Crea el prompt para el LLM

        Args:
            marca: Entidad de marca

        Returns:
            str: Prompt generado
        """
        return f"""
        Genera una descripción profesional para una marca de ganado bovino con las siguientes características:
        
        - Número de marca: {marca.numero_marca}
        - Productor: {marca.nombre_productor}
        - Raza: {marca.raza_bovino.value}
        - Propósito: {marca.proposito_ganado.value}
        - Cantidad de cabezas: {marca.cantidad_cabezas}
        - Departamento: {marca.departamento.value}
        - Municipio: {marca.municipio}
        
        La descripción debe ser:
        - Profesional y atractiva
        - Destacar las características únicas
        - Incluir información relevante del sector ganadero
        - Máximo 150 palabras
        """

    def _simular_generacion_llm(self, prompt: str, marca: MarcaGanadoBovino) -> str:
        """
        Simula la generación usando LLM

        Args:
            prompt: Prompt para el LLM
            marca: Entidad de marca

        Returns:
            str: Descripción generada
        """
        # En un entorno real, aquí se haría la llamada al LLM
        # Por ahora, generamos una descripción basada en los datos
        descripcion = (
            f"La marca {marca.numero_marca} representa una destacada operación ganadera "
            f"dirigida por {marca.nombre_productor}. Especializada en la producción de "
            f"{marca.proposito_ganado.value.lower()} con ganado de raza {marca.raza_bovino.value}, "
            f"esta estancia maneja {marca.cantidad_cabezas} cabezas de ganado en "
            f"{marca.municipio}, {marca.departamento.value}. "
            f"La operación refleja los más altos estándares de calidad y sostenibilidad "
            f"en el sector ganadero boliviano."
        )

        return descripcion

    def _generar_descripcion_fallback(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera descripción de respaldo si falla el LLM

        Args:
            marca: Entidad de marca

        Returns:
            str: Descripción de respaldo
        """
        return (
            f"Marca Bovina {marca.numero_marca} - {marca.nombre_productor}. "
            f"Ganado {marca.raza_bovino.value} para {marca.proposito_ganado.value.lower()}. "
            f"{marca.cantidad_cabezas} cabezas en {marca.municipio}, {marca.departamento.value}."
        )

    def generar_descripcion_para_marca_existente(self, marca: MarcaGanadoBovino) -> str:
        """
        Genera descripción para una marca existente

        Args:
            marca: Entidad de marca

        Returns:
            str: Descripción generada
        """
        return self._generar_descripcion_llm(marca)
