#!/usr/bin/env python3
"""
Script para crear las tablas en la base de datos ganaderia_bi
"""

import mysql.connector


def create_tables():
    """Crea las tablas en la base de datos"""

    # Consultas SQL para crear las tablas
    tables_sql = [
        # Tabla de marcas de ganado bovino
        """
        CREATE TABLE IF NOT EXISTS marca_ganado_bovino (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            numero_marca VARCHAR(50) UNIQUE NOT NULL,
            nombre_productor VARCHAR(255) NOT NULL,
            fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_procesamiento DATETIME NULL,
            estado ENUM('PENDIENTE', 'EN_PROCESO', 'APROBADO', 'RECHAZADO') NOT NULL DEFAULT 'PENDIENTE',
            monto_certificacion DECIMAL(15,2) NULL,
            raza_bovino VARCHAR(50) NOT NULL,
            proposito_ganado VARCHAR(50) NOT NULL,
            cantidad_cabezas INT NOT NULL DEFAULT 1,
            departamento VARCHAR(50) NOT NULL,
            municipio VARCHAR(100) NULL,
            comunidad VARCHAR(100) NULL,
            ci_productor VARCHAR(20) NULL,
            telefono_productor VARCHAR(20) NULL,
            tiempo_procesamiento_horas INT NULL,
            observaciones TEXT NULL,
            creado_por VARCHAR(100) NULL,
            actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        # Tabla de logos de marcas bovinas
        """
        CREATE TABLE IF NOT EXISTS logo_marca_bovina (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            marca_id BIGINT NOT NULL,
            url_logo VARCHAR(500) NULL,
            fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            exito BOOLEAN NOT NULL DEFAULT FALSE,
            tiempo_generacion_segundos INT NULL,
            modelo_ia_usado VARCHAR(50) NULL,
            prompt_usado TEXT NULL,
            calidad_logo ENUM('ALTA', 'MEDIA', 'BAJA') NULL,
            FOREIGN KEY (marca_id) REFERENCES marca_ganado_bovino(id) ON DELETE CASCADE
        )
        """,
        # Tabla de KPIs de ganado bovino
        """
        CREATE TABLE IF NOT EXISTS kpi_ganado_bovino (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            marcas_registradas_mes INT NOT NULL DEFAULT 0,
            tiempo_promedio_procesamiento DECIMAL(10,2) NOT NULL DEFAULT 0,
            porcentaje_aprobacion DECIMAL(5,2) NOT NULL DEFAULT 0,
            ingresos_mes DECIMAL(15,2) NOT NULL DEFAULT 0,
            total_cabezas_registradas INT NOT NULL DEFAULT 0,
            promedio_cabezas_por_marca DECIMAL(10,2) NOT NULL DEFAULT 0,
            marcas_carne INT NOT NULL DEFAULT 0,
            marcas_leche INT NOT NULL DEFAULT 0,
            marcas_doble_proposito INT NOT NULL DEFAULT 0,
            marcas_reproduccion INT NOT NULL DEFAULT 0,
            marcas_santa_cruz INT NOT NULL DEFAULT 0,
            marcas_beni INT NOT NULL DEFAULT 0,
            marcas_la_paz INT NOT NULL DEFAULT 0,
            marcas_otros_departamentos INT NOT NULL DEFAULT 0,
            tasa_exito_logos DECIMAL(5,2) NOT NULL DEFAULT 0,
            total_logos_generados INT NOT NULL DEFAULT 0,
            tiempo_promedio_generacion_logos DECIMAL(10,2) NOT NULL DEFAULT 0,
            UNIQUE KEY unique_fecha (fecha)
        )
        """,
        # Tabla de historial de estados de marcas
        """
        CREATE TABLE IF NOT EXISTS historial_estado_marca (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            marca_id BIGINT NOT NULL,
            estado_anterior VARCHAR(50) NULL,
            estado_nuevo VARCHAR(50) NOT NULL,
            fecha_cambio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            usuario_responsable VARCHAR(100) NOT NULL,
            observaciones_cambio TEXT NULL,
            FOREIGN KEY (marca_id) REFERENCES marca_ganado_bovino(id) ON DELETE CASCADE
        )
        """,
        # Tabla de datos del dashboard
        """
        CREATE TABLE IF NOT EXISTS dashboard_data (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            marcas_registradas_mes_actual INT NOT NULL DEFAULT 0,
            tiempo_promedio_procesamiento DECIMAL(10,2) NOT NULL DEFAULT 0,
            porcentaje_aprobacion DECIMAL(5,2) NOT NULL DEFAULT 0,
            porcentaje_rechazo DECIMAL(5,2) NOT NULL DEFAULT 0,
            ingresos_mes_actual DECIMAL(15,2) NOT NULL DEFAULT 0,
            total_cabezas_bovinas INT NOT NULL DEFAULT 0,
            promedio_cabezas_por_marca DECIMAL(10,2) NOT NULL DEFAULT 0,
            porcentaje_carne DECIMAL(5,2) NOT NULL DEFAULT 0,
            porcentaje_leche DECIMAL(5,2) NOT NULL DEFAULT 0,
            porcentaje_doble_proposito DECIMAL(5,2) NOT NULL DEFAULT 0,
            porcentaje_reproduccion DECIMAL(5,2) NOT NULL DEFAULT 0,
            raza_mas_comun VARCHAR(100) NULL,
            porcentaje_raza_principal DECIMAL(5,2) NOT NULL DEFAULT 0,
            tasa_exito_logos DECIMAL(5,2) NOT NULL DEFAULT 0,
            total_marcas_sistema INT NOT NULL DEFAULT 0,
            marcas_pendientes INT NOT NULL DEFAULT 0,
            alertas JSON NULL
        )
        """,
        # Tabla de datos de reportes
        """
        CREATE TABLE IF NOT EXISTS reporte_data (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            tipo_reporte VARCHAR(50) NOT NULL,
            periodo_inicio DATE NOT NULL,
            periodo_fin DATE NOT NULL,
            formato VARCHAR(20) NOT NULL DEFAULT 'json',
            datos JSON NOT NULL,
            usuario_generador VARCHAR(100) NULL
        )
        """,
    ]

    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="ganaderia_bi"
        )
        cursor = conn.cursor()

        print(" Conectado a la base de datos ganaderia_bi")

        # Crear cada tabla
        for i, sql in enumerate(tables_sql, 1):
            try:
                cursor.execute(sql)
                print(f"Tabla {i} creada correctamente")
            except mysql.connector.Error as e:
                print(f"Error creando tabla {i}: {e}")

        # Insertar datos de prueba
        insert_test_data(cursor)

        cursor.close()
        conn.close()

        print("Todas las tablas creadas correctamente!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def insert_test_data(cursor):
    """Inserta datos de prueba"""

    try:
        # Datos de prueba para marcas
        cursor.execute(
            """
            INSERT INTO marca_ganado_bovino (
                numero_marca, nombre_productor, estado, raza_bovino, proposito_ganado, 
                cantidad_cabezas, departamento, municipio, comunidad, ci_productor, 
                telefono_productor, monto_certificacion, creado_por
            ) VALUES 
            ('M001-2024', 'Juan Pérez', 'APROBADO', 'NELORE', 'CARNE', 50, 'SANTA_CRUZ', 'Montero', 'San José', '12345678', '70012345', 1500.00, 'admin'),
            ('M002-2024', 'María López', 'PENDIENTE', 'CRIOLLO', 'DOBLE_PROPOSITO', 25, 'BENI', 'Trinidad', 'El Carmen', '87654321', '70054321', 800.00, 'admin'),
            ('M003-2024', 'Carlos Rodríguez', 'EN_PROCESO', 'HOLSTEIN', 'LECHE', 30, 'LA_PAZ', 'El Alto', 'Villa Adela', '11223344', '70098765', 1200.00, 'admin')
        """
        )
        print("Datos de prueba insertados en marcas")

        # Datos de prueba para logos
        cursor.execute(
            """
            INSERT INTO logo_marca_bovina (
                marca_id, url_logo, exito, tiempo_generacion_segundos, modelo_ia_usado, 
                prompt_usado, calidad_logo
            ) VALUES 
            (1, 'https://example.com/logo1.png', TRUE, 45, 'DALL-E-3', 'Logo para marca ganadera Nelore', 'ALTA'),
            (2, 'https://example.com/logo2.png', FALSE, 30, 'GPT-4', 'Logo para marca ganadera Criollo', 'BAJA'),
            (3, 'https://example.com/logo3.png', TRUE, 60, 'MIDJOURNEY', 'Logo para marca ganadera Holstein', 'MEDIA')
        """
        )
        print("Datos de prueba insertados en logos")

        # Datos de prueba para KPIs
        cursor.execute(
            """
            INSERT INTO kpi_ganado_bovino (
                fecha, marcas_registradas_mes, tiempo_promedio_procesamiento, porcentaje_aprobacion,
                ingresos_mes, total_cabezas_registradas, promedio_cabezas_por_marca,
                marcas_carne, marcas_leche, marcas_doble_proposito, marcas_reproduccion,
                marcas_santa_cruz, marcas_beni, marcas_la_paz, marcas_otros_departamentos,
                tasa_exito_logos, total_logos_generados, tiempo_promedio_generacion_logos
            ) VALUES 
            ('2024-01-01', 3, 24.5, 60.0, 3500.00, 105, 35.0, 1, 1, 1, 0, 1, 1, 1, 0, 66.7, 3, 45.0)
        """
        )
        print("Datos de prueba insertados en KPIs")

        # Datos de prueba para dashboard
        cursor.execute(
            """
            INSERT INTO dashboard_data (
                marcas_registradas_mes_actual, tiempo_promedio_procesamiento, porcentaje_aprobacion,
                porcentaje_rechazo, ingresos_mes_actual, total_cabezas_bovinas, promedio_cabezas_por_marca,
                porcentaje_carne, porcentaje_leche, porcentaje_doble_proposito, porcentaje_reproduccion,
                raza_mas_comun, porcentaje_raza_principal, tasa_exito_logos, total_marcas_sistema, marcas_pendientes
            ) VALUES 
            (3, 24.5, 60.0, 0.0, 3500.00, 105, 35.0, 33.3, 33.3, 33.3, 0.0, 'NELORE', 33.3, 66.7, 3, 1)
        """
        )
        print("Datos de prueba insertados en dashboard")

    except mysql.connector.Error as e:
        print(f"Error insertando datos de prueba: {e}")


if __name__ == "__main__":
    print("Creando tablas en GanaderiaBi...")

    if create_tables():
        print("\nBase de datos configurada completamente!")
        print("Próximos pasos:")
        print("   1. Configurar Django settings.py")
        print("   2. Ejecutar: python manage.py migrate")
        print("   3. Crear superusuario: python manage.py createsuperuser")
        print("   4. Ejecutar el servidor: python manage.py runserver")
    else:
        print("Error configurando las tablas")
