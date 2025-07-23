"""
URL configuration for ganaderia_bi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Importar configuración del admin para Clean Architecture
import ganaderia_bi.admin_config


# Registrar las apps del admin manualmente para evitar el error NoReverseMatch
def register_admin_apps():
    """Registrar las apps del admin manualmente."""
    try:
        from apps.analytics.presentation.admin import (
            MarcaGanadoBovinoAdmin,
            LogoMarcaBovinaAdmin,
            KPIGanadoBovinoAdmin,
            HistorialEstadoMarcaAdmin,
            DashboardDataAdmin,
            ReporteDataAdmin,
        )

        from apps.analytics.infrastructure.models import (
            MarcaGanadoBovinoModel,
            LogoMarcaBovinaModel,
            KPIGanadoBovinoModel,
            HistorialEstadoMarcaModel,
            DashboardDataModel,
            ReporteDataModel,
        )

        # Registrar los modelos en el admin
        admin.site.register(MarcaGanadoBovinoModel, MarcaGanadoBovinoAdmin)
        admin.site.register(LogoMarcaBovinaModel, LogoMarcaBovinaAdmin)
        admin.site.register(KPIGanadoBovinoModel, KPIGanadoBovinoAdmin)
        admin.site.register(HistorialEstadoMarcaModel, HistorialEstadoMarcaAdmin)
        admin.site.register(DashboardDataModel, DashboardDataAdmin)
        admin.site.register(ReporteDataModel, ReporteDataAdmin)

    except Exception as e:
        print(f"Error registrando apps del admin: {e}")


# Registrar las apps del admin
register_admin_apps()

urlpatterns = [
    path("admin/", admin.site.urls),
    # URLs de la nueva arquitectura Clean Architecture
    path("api/analytics/", include("apps.analytics.presentation.urls")),
    # ✅ URLs de Documentación de APIs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Configuración de archivos estáticos y media para desarrollo
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
