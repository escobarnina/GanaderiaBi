"""
Implementación de repositorio de KPIs usando Django ORM
Responsabilidad única: Gestionar KPIs de ganado bovino
"""

from typing import List, Optional
from datetime import date

from apps.analytics.domain.entities.kpi_ganado_bovino import KPIGanadoBovino
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository

# Importar modelo Django de la nueva arquitectura
from apps.analytics.infrastructure.models import KPIGanadoBovinoModel


class DjangoKpiRepository(KPIGanadoBovinoRepository):
    """Implementación de repositorio de KPIs usando Django ORM
    Responsabilidad única: Gestionar KPIs de ganado bovino"""

    def _to_entity(self, model: KPIGanadoBovinoModel) -> KPIGanadoBovino:
        """Conversión de modelo Django a entidad de dominio"""
        return KPIGanadoBovino(
            id=model.id,
            fecha=model.fecha,
            marcas_registradas_mes=model.marcas_registradas_mes,
            tiempo_promedio_procesamiento=model.tiempo_promedio_procesamiento,
            porcentaje_aprobacion=model.porcentaje_aprobacion,
            ingresos_mes=model.ingresos_mes,
            total_cabezas_registradas=model.total_cabezas_registradas,
            promedio_cabezas_por_marca=model.promedio_cabezas_por_marca,
            marcas_carne=model.marcas_carne,
            marcas_leche=model.marcas_leche,
            marcas_doble_proposito=model.marcas_doble_proposito,
            marcas_reproduccion=model.marcas_reproduccion,
            marcas_santa_cruz=model.marcas_santa_cruz,
            marcas_beni=model.marcas_beni,
            marcas_la_paz=model.marcas_la_paz,
            marcas_otros_departamentos=model.marcas_otros_departamentos,
            tasa_exito_logos=model.tasa_exito_logos,
            total_logos_generados=model.total_logos_generados,
            tiempo_promedio_generacion_logos=model.tiempo_promedio_generacion_logos,
        )

    def _to_model(self, entity: KPIGanadoBovino) -> KPIGanadoBovinoModel:
        """Conversión de entidad de dominio a modelo Django"""
        model_data = {
            "fecha": entity.fecha,
            "marcas_registradas_mes": entity.marcas_registradas_mes,
            "tiempo_promedio_procesamiento": entity.tiempo_promedio_procesamiento,
            "porcentaje_aprobacion": entity.porcentaje_aprobacion,
            "ingresos_mes": entity.ingresos_mes,
            "total_cabezas_registradas": entity.total_cabezas_registradas,
            "promedio_cabezas_por_marca": entity.promedio_cabezas_por_marca,
            "marcas_carne": entity.marcas_carne,
            "marcas_leche": entity.marcas_leche,
            "marcas_doble_proposito": entity.marcas_doble_proposito,
            "marcas_reproduccion": entity.marcas_reproduccion,
            "marcas_santa_cruz": entity.marcas_santa_cruz,
            "marcas_beni": entity.marcas_beni,
            "marcas_la_paz": entity.marcas_la_paz,
            "marcas_otros_departamentos": entity.marcas_otros_departamentos,
            "tasa_exito_logos": entity.tasa_exito_logos,
            "total_logos_generados": entity.total_logos_generados,
            "tiempo_promedio_generacion_logos": entity.tiempo_promedio_generacion_logos,
        }

        if entity.id:
            model = KPIGanadoBovinoModel.objects.get(id=entity.id)
            for key, value in model_data.items():
                setattr(model, key, value)
            return model
        else:
            return KPIGanadoBovinoModel(**model_data)

    def crear(self, kpi: KPIGanadoBovino) -> KPIGanadoBovino:
        """Implementa KPIGanadoBovinoRepository.save (crear)"""
        model = self._to_model(kpi)
        model.save()
        return self._to_entity(model)

    def obtener_por_fecha(self, fecha: date) -> Optional[KPIGanadoBovino]:
        """Implementa KPIGanadoBovinoRepository.get_by_fecha"""
        try:
            model = KPIGanadoBovinoModel.objects.get(fecha=fecha)
            return self._to_entity(model)
        except KPIGanadoBovinoModel.DoesNotExist:
            return None

    def obtener_por_id(self, kpi_id: int) -> Optional[KPIGanadoBovino]:
        """Implementa KPIGanadoBovinoRepository.get_by_id"""
        try:
            model = KPIGanadoBovinoModel.objects.get(id=kpi_id)
            return self._to_entity(model)
        except KPIGanadoBovinoModel.DoesNotExist:
            return None

    def actualizar(self, kpi: KPIGanadoBovino) -> KPIGanadoBovino:
        """Implementa KPIGanadoBovinoRepository.save (actualizar)"""
        model = self._to_model(kpi)
        model.save()
        return self._to_entity(model)

    def eliminar(self, kpi_id: int) -> bool:
        """Implementa KPIGanadoBovinoRepository.delete"""
        try:
            model = KPIGanadoBovinoModel.objects.get(id=kpi_id)
            model.delete()
            return True
        except KPIGanadoBovinoModel.DoesNotExist:
            return False

    def listar_todos(self, limit: int = 100, offset: int = 0) -> List[KPIGanadoBovino]:
        """Implementa KPIGanadoBovinoRepository.list_all"""
        models = KPIGanadoBovinoModel.objects.all()[offset : offset + limit]
        return [self._to_entity(model) for model in models]

    def listar_por_rango_fechas(
        self, fecha_inicio: date, fecha_fin: date
    ) -> List[KPIGanadoBovino]:
        """Implementa KPIGanadoBovinoRepository.list_by_periodo"""
        models = KPIGanadoBovinoModel.objects.filter(
            fecha__gte=fecha_inicio, fecha__lte=fecha_fin
        ).order_by("-fecha")
        return [self._to_entity(model) for model in models]

    def obtener_ultimo_kpi(self) -> Optional[KPIGanadoBovino]:
        """Implementa KPIGanadoBovinoRepository.get_latest"""
        try:
            model = KPIGanadoBovinoModel.objects.latest("fecha")
            return self._to_entity(model)
        except KPIGanadoBovinoModel.DoesNotExist:
            return None

    def obtener_tendencias_mensuales(self, meses: int = 12) -> List[KPIGanadoBovino]:
        """Implementa KPIGanadoBovinoRepository.list_by_periodo (mensual)"""
        from django.utils import timezone
        from datetime import timedelta

        fecha_limite = timezone.now().date() - timedelta(days=meses * 30)
        models = KPIGanadoBovinoModel.objects.filter(fecha__gte=fecha_limite).order_by(
            "-fecha"
        )
        return [self._to_entity(model) for model in models]

    def calcular_kpi_diario(self, fecha: date) -> KPIGanadoBovino:
        """Implementa KPIGanadoBovinoRepository.calcular_kpis_actuales"""
        from django.db.models import Count, Avg, Sum
        from apps.analytics.infrastructure.models import (
            MarcaGanadoBovinoModel,
            LogoMarcaBovinaModel,
        )
        from apps.analytics.domain.enums import EstadoMarca

        # Obtener datos del día
        marcas_dia = MarcaGanadoBovinoModel.objects.filter(fecha_registro__date=fecha)

        # KPIs principales
        marcas_registradas = marcas_dia.count()
        marcas_aprobadas = marcas_dia.filter(estado=EstadoMarca.APROBADO.value).count()
        tiempo_promedio = (
            marcas_dia.aggregate(promedio=Avg("tiempo_procesamiento_horas"))["promedio"]
            or 0
        )
        ingresos = marcas_dia.aggregate(total=Sum("monto_certificacion"))["total"] or 0
        total_cabezas = (
            marcas_dia.aggregate(total=Sum("cantidad_cabezas"))["total"] or 0
        )

        # Distribución por propósito
        marcas_carne = marcas_dia.filter(proposito_ganado="CARNE").count()
        marcas_leche = marcas_dia.filter(proposito_ganado="LECHE").count()
        marcas_doble_proposito = marcas_dia.filter(
            proposito_ganado="DOBLE_PROPOSITO"
        ).count()
        marcas_reproduccion = marcas_dia.filter(proposito_ganado="REPRODUCCION").count()

        # Distribución por departamento
        marcas_santa_cruz = marcas_dia.filter(departamento="SANTA_CRUZ").count()
        marcas_beni = marcas_dia.filter(departamento="BENI").count()
        marcas_la_paz = marcas_dia.filter(departamento="LA_PAZ").count()
        marcas_otros = marcas_dia.exclude(
            departamento__in=["SANTA_CRUZ", "BENI", "LA_PAZ"]
        ).count()

        # KPIs de logos
        logos_dia = LogoMarcaBovinaModel.objects.filter(fecha_generacion__date=fecha)
        total_logos = logos_dia.count()
        logos_exitosos = logos_dia.filter(exito=True).count()
        tasa_exito_logos = (
            (logos_exitosos / total_logos * 100) if total_logos > 0 else 0
        )
        tiempo_promedio_logos = (
            logos_dia.aggregate(promedio=Avg("tiempo_generacion_segundos"))["promedio"]
            or 0
        )

        return KPIGanadoBovino(
            fecha=fecha,
            marcas_registradas_mes=marcas_registradas,
            tiempo_promedio_procesamiento=tiempo_promedio,
            porcentaje_aprobacion=(
                (marcas_aprobadas / marcas_registradas * 100)
                if marcas_registradas > 0
                else 0
            ),
            ingresos_mes=ingresos,
            total_cabezas_registradas=total_cabezas,
            promedio_cabezas_por_marca=(
                (total_cabezas / marcas_registradas) if marcas_registradas > 0 else 0
            ),
            marcas_carne=marcas_carne,
            marcas_leche=marcas_leche,
            marcas_doble_proposito=marcas_doble_proposito,
            marcas_reproduccion=marcas_reproduccion,
            marcas_santa_cruz=marcas_santa_cruz,
            marcas_beni=marcas_beni,
            marcas_la_paz=marcas_la_paz,
            marcas_otros_departamentos=marcas_otros,
            tasa_exito_logos=tasa_exito_logos,
            total_logos_generados=total_logos,
            tiempo_promedio_generacion_logos=tiempo_promedio_logos,
        )
