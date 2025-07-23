#!/usr/bin/env python3
"""
Script corregido para insertar datos de prueba en la base de datos ganaderia_bi
"""

import mysql.connector


def insert_test_data():
    """Inserta datos de prueba en la base de datos"""

    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="ganaderia_bi"
        )
        cursor = conn.cursor()

        print(" Conectado a la base de datos ganaderia_bi")

        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM marca_ganado_bovino")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Ya hay {count} marcas en la base de datos")
            return True

        # Insertar datos de prueba para marcas
        cursor.execute(
            """
            INSERT INTO marca_ganado_bovino (
                numero_marca, nombre_productor, estado, raza_bovino, proposito_ganado, 
                cantidad_cabezas, departamento, municipio, comunidad, ci_productor, 
                telefono_productor, monto_certificacion, creado_por
            ) VALUES 
            ('M001-2024', 'Juan Pérez', 'APROBADO', 'NELORE', 'CARNE', 50, 'SANTA_CRUZ', 'Montero', 'San José', '12345678', '70012345', 1500.00, 'admin'),
            ('M002-2024', 'María López', 'PENDIENTE', 'CRIOLLO', 'DOBLE_PROPOSITO', 25, 'BENI', 'Trinidad', 'El Carmen', '87654321', '70054321', 800.00, 'admin'),
            ('M003-2024', 'Carlos Rodríguez', 'EN_PROCESO', 'HOLSTEIN', 'LECHE', 30, 'LA_PAZ', 'El Alto', 'Villa Adela', '11223344', '70098765', 1200.00, 'admin'),
            ('M004-2024', 'Ana Martínez', 'APROBADO', 'BRAHMAN', 'CARNE', 40, 'SANTA_CRUZ', 'Warnes', 'La Esperanza', '55667788', '70011111', 1000.00, 'admin'),
            ('M005-2024', 'Luis García', 'RECHAZADO', 'ANGUS', 'REPRODUCCION', 15, 'COCHABAMBA', 'Quillacollo', 'San Pedro', '99887766', '70022222', 600.00, 'admin')
        """
        )
        print("5 marcas insertadas")

        # Obtener los IDs de las marcas insertadas
        cursor.execute("SELECT id, numero_marca FROM marca_ganado_bovino ORDER BY id")
        marcas = cursor.fetchall()

        print("IDs de marcas obtenidos:")
        for marca_id, numero_marca in marcas:
            print(f"  - ID {marca_id}: {numero_marca}")

        # Insertar datos de prueba para logos usando los IDs reales
        for marca_id, numero_marca in marcas[:4]:  # Solo las primeras 4 marcas
            cursor.execute(
                """
                INSERT INTO logo_marca_bovina (
                    marca_id, url_logo, exito, tiempo_generacion_segundos, modelo_ia_usado, 
                    prompt_usado, calidad_logo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    marca_id,
                    f"https://example.com/logo{marca_id}.png",
                    True if marca_id % 2 == 1 else False,  # Alternar éxito
                    30 + marca_id * 5,
                    "DALL-E-3" if marca_id % 2 == 1 else "GPT-4",
                    f"Logo para marca ganadera {numero_marca}",
                    "ALTA" if marca_id % 2 == 1 else "MEDIA",
                ),
            )

        print("4 logos insertados")

        # Insertar datos de prueba para KPIs
        cursor.execute(
            """
            INSERT INTO kpi_ganado_bovino (
                fecha, marcas_registradas_mes, tiempo_promedio_procesamiento, porcentaje_aprobacion,
                ingresos_mes, total_cabezas_registradas, promedio_cabezas_por_marca,
                marcas_carne, marcas_leche, marcas_doble_proposito, marcas_reproduccion,
                marcas_santa_cruz, marcas_beni, marcas_la_paz, marcas_otros_departamentos,
                tasa_exito_logos, total_logos_generados, tiempo_promedio_generacion_logos
            ) VALUES 
            ('2024-01-01', 5, 24.5, 60.0, 5100.00, 160, 32.0, 2, 1, 1, 1, 2, 1, 1, 1, 75.0, 4, 43.75)
        """
        )
        print("1 KPI insertado")

        # Insertar datos de prueba para historial usando los IDs reales
        for marca_id, numero_marca in marcas:
            # Historial para cada marca
            cursor.execute(
                """
                INSERT INTO historial_estado_marca (
                    marca_id, estado_anterior, estado_nuevo, usuario_responsable, observaciones_cambio
                ) VALUES (%s, %s, %s, %s, %s)
            """,
                (marca_id, None, "PENDIENTE", "admin", f"Marca {numero_marca} creada"),
            )

            # Si la marca está aprobada, agregar más historial
            if marca_id in [1, 4]:  # Marcas aprobadas
                cursor.execute(
                    """
                    INSERT INTO historial_estado_marca (
                        marca_id, estado_anterior, estado_nuevo, usuario_responsable, observaciones_cambio
                    ) VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        marca_id,
                        "PENDIENTE",
                        "EN_PROCESO",
                        "admin",
                        f"Procesando marca {numero_marca}",
                    ),
                )

                cursor.execute(
                    """
                    INSERT INTO historial_estado_marca (
                        marca_id, estado_anterior, estado_nuevo, usuario_responsable, observaciones_cambio
                    ) VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        marca_id,
                        "EN_PROCESO",
                        "APROBADO",
                        "admin",
                        f"Marca {numero_marca} aprobada",
                    ),
                )

            # Si la marca está en proceso
            elif marca_id == 3:
                cursor.execute(
                    """
                    INSERT INTO historial_estado_marca (
                        marca_id, estado_anterior, estado_nuevo, usuario_responsable, observaciones_cambio
                    ) VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        marca_id,
                        "PENDIENTE",
                        "EN_PROCESO",
                        "admin",
                        f"Procesando marca {numero_marca}",
                    ),
                )

            # Si la marca está rechazada
            elif marca_id == 5:
                cursor.execute(
                    """
                    INSERT INTO historial_estado_marca (
                        marca_id, estado_anterior, estado_nuevo, usuario_responsable, observaciones_cambio
                    ) VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        marca_id,
                        "PENDIENTE",
                        "RECHAZADO",
                        "admin",
                        f"Marca {numero_marca} rechazada",
                    ),
                )

        print("Historial insertado para todas las marcas")

        # Insertar datos de prueba para dashboard
        cursor.execute(
            """
            INSERT INTO dashboard_data (
                marcas_registradas_mes_actual, tiempo_promedio_procesamiento, porcentaje_aprobacion,
                porcentaje_rechazo, ingresos_mes_actual, total_cabezas_bovinas, promedio_cabezas_por_marca,
                porcentaje_carne, porcentaje_leche, porcentaje_doble_proposito, porcentaje_reproduccion,
                raza_mas_comun, porcentaje_raza_principal, tasa_exito_logos, total_marcas_sistema, marcas_pendientes
            ) VALUES 
            (5, 24.5, 60.0, 20.0, 5100.00, 160, 32.0, 40.0, 20.0, 20.0, 20.0, 'NELORE', 40.0, 75.0, 5, 1)
        """
        )
        print("1 registro de dashboard insertado")

        # Insertar datos de prueba para reportes
        cursor.execute(
            """
            INSERT INTO reporte_data (
                tipo_reporte, periodo_inicio, periodo_fin, formato, datos, usuario_generador
            ) VALUES 
            ('REPORTE_MENSUAL', '2024-01-01', '2024-01-31', 'json', '{"marcas": 5, "ingresos": 5100.00}', 'admin'),
            ('REPORTE_ANUAL', '2024-01-01', '2024-12-31', 'excel', '{"marcas": 5, "ingresos": 5100.00}', 'admin')
        """
        )
        print("2 reportes insertados")

        # Confirmar cambios
        conn.commit()

        cursor.close()
        conn.close()

        print("Datos de prueba insertados correctamente!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def verify_data():
    """Verifica los datos insertados"""

    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="ganaderia_bi"
        )
        cursor = conn.cursor()

        # Verificar marcas
        cursor.execute("SELECT COUNT(*) FROM marca_ganado_bovino")
        marcas_count = cursor.fetchone()[0]

        # Verificar logos
        cursor.execute("SELECT COUNT(*) FROM logo_marca_bovina")
        logos_count = cursor.fetchone()[0]

        # Verificar KPIs
        cursor.execute("SELECT COUNT(*) FROM kpi_ganado_bovino")
        kpis_count = cursor.fetchone()[0]

        # Verificar historial
        cursor.execute("SELECT COUNT(*) FROM historial_estado_marca")
        historial_count = cursor.fetchone()[0]

        # Verificar dashboard
        cursor.execute("SELECT COUNT(*) FROM dashboard_data")
        dashboard_count = cursor.fetchone()[0]

        # Verificar reportes
        cursor.execute("SELECT COUNT(*) FROM reporte_data")
        reportes_count = cursor.fetchone()[0]

        print(" Verificación de datos:")
        print(f"  - Marcas: {marcas_count}")
        print(f"  - Logos: {logos_count}")
        print(f"  - KPIs: {kpis_count}")
        print(f"  - Historial: {historial_count}")
        print(f"  - Dashboard: {dashboard_count}")
        print(f"  - Reportes: {reportes_count}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error verificando datos: {e}")


if __name__ == "__main__":
    print("Insertando datos de prueba en GanaderiaBi (Corregido)...")

    if insert_test_data():
        print("\nDatos insertados correctamente!")
        verify_data()
    else:
        print("Error insertando datos")
