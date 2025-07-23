# ganaderia_bi/settings.py
"""
Configuración simplificada para el microservicio de Business Intelligence.
Configuración única para desarrollo y testing.
"""

import os
from pathlib import Path

# Configurar PyMySQL ANTES de cualquier importación de Django
import pymysql

pymysql.install_as_MySQLdb()

# Configuración de compatibilidad con MariaDB 10.4
import pymysql.cursors

pymysql.cursors.DictCursor = pymysql.cursors.Cursor

# Importar configuración de compatibilidad con MariaDB
try:
    import db_compatibility
except ImportError:
    pass

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-change-me-in-production-123456789"
)

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",  # ✅ API Documentation
    "apps.analytics",  # ✅ Nueva app con Clean Architecture - IMPLEMENTADA
]

# Configuración del sitio administrativo
ADMIN_SITE_HEADER = (
    "🐄 Administración - Sistema de Marcas Ganaderas Bovinas (Clean Architecture)"
)
ADMIN_SITE_TITLE = "Ganado Bovino Admin"
ADMIN_INDEX_TITLE = "Panel de Control - Inteligencia de Negocios Ganadera"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Database - MariaDB 10.5 para desarrollo con XAMPP
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ganaderia_bi",
        "USER": "root",
        "PASSWORD": "",  # Sin contraseña por defecto en XAMPP
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "sql_mode": "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO",
            "charset": "utf8mb4",
            "use_unicode": True,
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO'",
            "autocommit": True,
            "isolation_level": "READ COMMITTED",
        },
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_ALL_ORIGINS = True

# Internationalization
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/La_Paz"
USE_I18N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración específica para MariaDB - Deshabilitar RETURNING
DJANGO_DB_OPTIONS = {
    "mysql": {
        "supports_returning": False,
    }
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "apps.analytics": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Configuración de APIs externas (para futuras integraciones)
AFILIADOS_API_URL = config(
    "AFILIADOS_API_URL", default="http://localhost:8001/api/afiliados/v1/"
)
GANADO_API_URL = config(
    "GANADO_API_URL", default="http://localhost:8002/api/ganado/v1/"
)
CERTIFICADOS_API_URL = config(
    "CERTIFICADOS_API_URL", default="http://localhost:8003/api/certificados/v1/"
)
IA_API_URL = config("IA_API_URL", default="http://localhost:8004/api/ia/v1/")

# ✅ Configuraciones para Clean Architecture (IMPLEMENTADAS)
# Configuración de Redis para Celery
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

# ✅ Configuración de Documentación de APIs (IMPLEMENTADA)
SPECTACULAR_SETTINGS = {
    "TITLE": "🐄 API de Inteligencia de Negocios Ganadero",
    "DESCRIPTION": """
    Sistema de inteligencia de negocios para la gestión de ganado bovino.
    
    ## Funcionalidades Principales:
    - **Gestión de Marcas**: CRUD completo de marcas de ganado
    - **Generación de Logos**: Logos generados por IA
    - **Dashboard y KPIs**: Métricas y análisis ejecutivo
    - **Reportes**: Reportes especializados del sector
    - **Historial**: Auditoría y trazabilidad de cambios
    - **Analytics**: Análisis avanzado y tendencias
    
    ## Arquitectura:
    - Clean Architecture implementada
    - Principios SOLID aplicados
    - Preparado para microservicios
    """,
    "VERSION": "2.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/analytics/",
    "TAGS": [
        {"name": "marcas", "description": "Gestión de marcas de ganado bovino"},
        {"name": "logos", "description": "Generación y gestión de logos con IA"},
        {"name": "dashboard", "description": "Dashboard ejecutivo y métricas"},
        {"name": "kpis", "description": "Indicadores clave de rendimiento"},
        {"name": "historial", "description": "Auditoría y trazabilidad"},
        {"name": "reportes", "description": "Reportes especializados"},
        {"name": "estadisticas", "description": "Análisis estadístico"},
        {"name": "data-generation", "description": "Generación de datos de prueba"},
    ],
    "CONTACT": {
        "name": "Equipo BI/AI/Agentes",
        "email": "bi@ganaderia.com",
    },
    "LICENSE": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
}

# Configuración de Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE

# Configuración de cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# Configuración de JWT
JWT_PUBLIC_KEY = config("JWT_PUBLIC_KEY", default="")
JWT_PRIVATE_KEY = config("JWT_PRIVATE_KEY", default="")

# Configuración de sesiones para desarrollo
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
