.PHONY: help install test lint format clean migrate runserver shell

# Variables
PYTHON = python
PIP = pip
MANAGE = python manage.py

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	$(PIP) install -r requirements.txt

install-dev: ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements.txt

test: ## Ejecutar tests
	pytest

test-cov: ## Ejecutar tests con coverage
	pytest --cov=apps --cov=business_intelligence --cov-report=html

test-unit: ## Ejecutar tests unitarios
	pytest -m unit

test-integration: ## Ejecutar tests de integración
	pytest -m integration

lint: ## Ejecutar linting
	flake8 apps/ business_intelligence/
	black --check apps/ business_intelligence/
	mypy apps/ business_intelligence/

format: ## Formatear código
	black apps/ business_intelligence/
	isort apps/ business_intelligence/

format-check: ## Verificar formato
	black --check apps/ business_intelligence/
	isort --check-only apps/ business_intelligence/

migrate: ## Ejecutar migraciones
	$(MANAGE) makemigrations
	$(MANAGE) migrate

migrate-reset: ## Resetear migraciones
	$(MANAGE) migrate --fake-initial
	$(MANAGE) migrate

runserver: ## Ejecutar servidor de desarrollo
	$(MANAGE) runserver

runserver-prod: ## Ejecutar servidor de producción
	$(MANAGE) runserver 0.0.0.0:8000

shell: ## Abrir shell de Django
	$(MANAGE) shell

dbshell: ## Abrir shell de base de datos
	$(MANAGE) dbshell

createsuperuser: ## Crear superusuario
	$(MANAGE) createsuperuser

collectstatic: ## Recolectar archivos estáticos
	$(MANAGE) collectstatic --noinput

generate-data: ## Generar datos de prueba
	$(MANAGE) generar_datos --marcas 100 --logos 80

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -name ".coverage" -delete

clean-db: ## Limpiar base de datos
	$(MANAGE) flush --noinput

reset: clean clean-db migrate generate-data ## Reset completo del proyecto

logs: ## Ver logs de la aplicación
	tail -f logs/django.log

check: format lint test ## Verificar todo (formato, linting, tests)

pre-commit: format lint test ## Comando para pre-commit hook

setup-dev: install-dev migrate generate-data ## Configurar entorno de desarrollo completo

# ✅ Comandos para Clean Architecture (IMPLEMENTADOS)
celery-worker: ## Ejecutar worker de Celery
	celery -A ganaderia_bi worker -l info

celery-beat: ## Ejecutar beat de Celery
	celery -A ganaderia_bi beat -l info

# TODO: Comandos para Fase 3 (Use Cases y Presentation)
# Descomentar cuando se implemente la nueva arquitectura:

# docker-build: ## Construir imagen Docker
# 	docker build -t ganaderia-bi .
# 
# docker-run: ## Ejecutar contenedor Docker
# 	docker run -p 8000:8000 ganaderia-bi
# 
# docker-compose-up: ## Levantar servicios con Docker Compose
# 	docker-compose up -d
# 
# docker-compose-down: ## Bajar servicios con Docker Compose
# 	docker-compose down

security: ## Verificar seguridad
	bandit -r business_intelligence/
	safety check 