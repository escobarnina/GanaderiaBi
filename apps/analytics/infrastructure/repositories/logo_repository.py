"""
Implementación de repositorio de logos usando Django ORM
Responsabilidad única: Gestionar logos de marcas bovinas
"""

from typing import List, Optional, Dict, Any
from django.db import models
from django.utils import timezone

from apps.analytics.domain.entities.logo_marca_bovina import LogoMarcaBovina
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import ModeloIA, CalidadLogo

# Importar modelo Django de la nueva arquitectura
from apps.analytics.infrastructure.models import LogoMarcaBovinaModel


class DjangoLogoRepository(LogoMarcaBovinaRepository):
    """Implementación de repositorio de logos usando Django ORM
    Responsabilidad única: Gestionar logos de marcas bovinas"""

    def _to_entity(self, model: LogoMarcaBovinaModel) -> LogoMarcaBovina:
        """Convierte modelo Django a entidad de dominio"""
        return LogoMarcaBovina(
            id=model.id,
            marca_id=model.marca_id,
            url_logo=model.url_logo,
            fecha_generacion=model.fecha_generacion,
            exito=model.exito,
            tiempo_generacion_segundos=model.tiempo_generacion_segundos,
            modelo_ia_usado=ModeloIA(model.modelo_ia_usado),
            prompt_usado=model.prompt_usado,
            calidad_logo=CalidadLogo(model.calidad_logo),
        )

    def _to_model(self, entity: LogoMarcaBovina) -> LogoMarcaBovinaModel:
        """Convierte entidad de dominio a modelo Django"""
        model_data = {
            "marca_id": entity.marca_id,
            "url_logo": entity.url_logo,
            "fecha_generacion": entity.fecha_generacion,
            "exito": entity.exito,
            "tiempo_generacion_segundos": entity.tiempo_generacion_segundos,
            "modelo_ia_usado": entity.modelo_ia_usado.value,
            "prompt_usado": entity.prompt_usado,
            "calidad_logo": entity.calidad_logo.value,
        }

        if entity.id:
            model = LogoMarcaBovinaModel.objects.get(id=entity.id)
            for key, value in model_data.items():
                setattr(model, key, value)
            return model
        else:
            return LogoMarcaBovinaModel(**model_data)

    def crear(self, logo: LogoMarcaBovina) -> LogoMarcaBovina:
        """Crea un nuevo logo"""
        model = self._to_model(logo)
        model.save()
        return self._to_entity(model)

    def obtener_por_id(self, logo_id: int) -> Optional[LogoMarcaBovina]:
        """Obtiene un logo por su ID"""
        try:
            model = LogoMarcaBovinaModel.objects.get(id=logo_id)
            return self._to_entity(model)
        except LogoMarcaBovinaModel.DoesNotExist:
            return None

    def obtener_por_marca(self, marca_id: int) -> List[LogoMarcaBovina]:
        """Obtiene todos los logos de una marca"""
        models = LogoMarcaBovinaModel.objects.filter(marca_id=marca_id).order_by(
            "-fecha_generacion"
        )
        return [self._to_entity(model) for model in models]

    def actualizar(self, logo: LogoMarcaBovina) -> LogoMarcaBovina:
        """Actualiza un logo existente"""
        model = self._to_model(logo)
        model.save()
        return self._to_entity(model)

    def eliminar(self, logo_id: int) -> bool:
        """Elimina un logo"""
        try:
            model = LogoMarcaBovinaModel.objects.get(id=logo_id)
            model.delete()
            return True
        except LogoMarcaBovinaModel.DoesNotExist:
            return False

    def listar_todos(self, limit: int = 100, offset: int = 0) -> List[LogoMarcaBovina]:
        """Lista todos los logos con paginación"""
        models = LogoMarcaBovinaModel.objects.all()[offset : offset + limit]
        return [self._to_entity(model) for model in models]

    def listar_exitosos(self) -> List[LogoMarcaBovina]:
        """Lista logos generados exitosamente"""
        models = LogoMarcaBovinaModel.objects.filter(exito=True)
        return [self._to_entity(model) for model in models]

    def listar_por_modelo_ia(self, modelo: ModeloIA) -> List[LogoMarcaBovina]:
        """Lista logos por modelo de IA"""
        models = LogoMarcaBovinaModel.objects.filter(modelo_ia_usado=modelo.value)
        return [self._to_entity(model) for model in models]

    def listar_por_calidad(self, calidad: CalidadLogo) -> List[LogoMarcaBovina]:
        """Lista logos por calidad"""
        models = LogoMarcaBovinaModel.objects.filter(calidad_logo=calidad.value)
        return [self._to_entity(model) for model in models]

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas de logos"""
        from django.db.models import Count, Avg

        total_logos = LogoMarcaBovinaModel.objects.count()
        logos_exitosos = LogoMarcaBovinaModel.objects.filter(exito=True).count()
        tasa_exito = (logos_exitosos / total_logos * 100) if total_logos > 0 else 0

        # Estadísticas por modelo de IA
        modelos = LogoMarcaBovinaModel.objects.values("modelo_ia_usado").annotate(
            total=Count("id"), exitosos=Count("id", filter=models.Q(exito=True))
        )

        # Estadísticas por calidad
        calidades = LogoMarcaBovinaModel.objects.values("calidad_logo").annotate(
            total=Count("id")
        )

        # Tiempo promedio de generación
        tiempo_promedio = (
            LogoMarcaBovinaModel.objects.aggregate(
                promedio=Avg("tiempo_generacion_segundos")
            )["promedio"]
            or 0
        )

        return {
            "total_logos": total_logos,
            "logos_exitosos": logos_exitosos,
            "tasa_exito": tasa_exito,
            "tiempo_promedio_generacion": tiempo_promedio,
            "modelos": {
                m["modelo_ia_usado"]: {"total": m["total"], "exitosos": m["exitosos"]}
                for m in modelos
            },
            "calidades": {c["calidad_logo"]: c["total"] for c in calidades},
        }

    def obtener_rendimiento_modelos(self) -> List[Dict[str, Any]]:
        """Obtiene rendimiento por modelo de IA"""
        from django.db.models import Count, Avg

        rendimiento = LogoMarcaBovinaModel.objects.values("modelo_ia_usado").annotate(
            total_generados=Count("id"),
            exitosos=Count("id", filter=models.Q(exito=True)),
            tiempo_promedio=Avg("tiempo_generacion_segundos"),
            alta_calidad=Count("id", filter=models.Q(calidad_logo="ALTA")),
            media_calidad=Count("id", filter=models.Q(calidad_logo="MEDIA")),
            baja_calidad=Count("id", filter=models.Q(calidad_logo="BAJA")),
        )

        return [
            {
                "modelo_ia_usado": item["modelo_ia_usado"],
                "total_generados": item["total_generados"],
                "exitosos": item["exitosos"],
                "fallidos": item["total_generados"] - item["exitosos"],
                "tasa_exito": (
                    (item["exitosos"] / item["total_generados"] * 100)
                    if item["total_generados"] > 0
                    else 0
                ),
                "tiempo_promedio_generacion": item["tiempo_promedio"] or 0,
                "logos_alta_calidad": item["alta_calidad"],
                "logos_media_calidad": item["media_calidad"],
                "logos_baja_calidad": item["baja_calidad"],
                "porcentaje_alta_calidad": (
                    (item["alta_calidad"] / item["total_generados"] * 100)
                    if item["total_generados"] > 0
                    else 0
                ),
            }
            for item in rendimiento
        ]
