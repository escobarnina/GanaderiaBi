#!/usr/bin/env python3
"""
Script para configurar la base de datos de GanaderiaBi
"""

import mysql.connector
import os
from pathlib import Path


def setup_database():
    """Configura la base de datos completa"""

    # Configuración de conexión
    config = {
        "host": "localhost",
        "user": "root",  # Usuario root para crear BD
        "password": "",  # Sin contraseña por defecto
        "charset": "utf8mb4",
    }

    try:
        # Conectar a MySQL
        print("🔌 Conectando a MySQL...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Leer el script SQL
        script_path = Path(__file__).parent / "create_database_structure.sql"
        print(f"📖 Leyendo script: {script_path}")

        with open(script_path, "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Ejecutar el script
        print("🚀 Ejecutando script de creación de base de datos...")

        # Dividir el script en comandos individuales
        commands = sql_script.split(";")

        for command in commands:
            command = command.strip()
            if command and not command.startswith("--"):
                try:
                    cursor.execute(command)
                    print(f"✅ Ejecutado: {command[:50]}...")
                except mysql.connector.Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️  Advertencia: {e}")

        # Confirmar cambios
        connection.commit()
        print("✅ Base de datos configurada exitosamente!")

        # Verificar tablas creadas
        cursor.execute("USE ganaderia_bi")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print(f"📊 Tablas creadas: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")

        return True

    except mysql.connector.Error as e:
        print(f"❌ Error de MySQL: {e}")
        return False

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {script_path}")
        return False

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")


def test_connection():
    """Prueba la conexión con la nueva base de datos"""

    config = {
        "host": "localhost",
        "user": "bi_user",
        "password": "password",
        "database": "ganaderia_bi",
        "charset": "utf8mb4",
    }

    try:
        print("🧪 Probando conexión con la nueva base de datos...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Probar consulta
        cursor.execute("SELECT COUNT(*) FROM marca_ganado_bovino")
        count = cursor.fetchone()[0]

        print(f"✅ Conexión exitosa! Marcas en BD: {count}")

        cursor.close()
        connection.close()
        return True

    except mysql.connector.Error as e:
        print(f"❌ Error de conexión: {e}")
        return False


def main():
    """Función principal"""
    print("🐄 Configurador de Base de Datos GanaderiaBi")
    print("=" * 50)

    # Configurar base de datos
    if setup_database():
        print("\n🎉 Base de datos configurada correctamente!")

        # Probar conexión
        if test_connection():
            print("✅ Todo listo para usar!")
        else:
            print("⚠️  La base de datos se creó pero hay problemas de conexión")
    else:
        print("\n❌ Error configurando la base de datos")
        return False

    print("\n📋 Próximos pasos:")
    print("   1. Configurar Django settings.py con las credenciales")
    print("   2. Ejecutar: python manage.py migrate")
    print("   3. Crear superusuario: python manage.py createsuperuser")
    print("   4. Ejecutar el servidor: python manage.py runserver")

    return True


if __name__ == "__main__":
    main()
