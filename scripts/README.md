# 🗄️ Scripts de Configuración de Base de Datos - GanaderiaBi

## 📋 **Descripción**

Este directorio contiene los scripts esenciales para configurar la base de datos de GanaderiaBi con Clean Architecture.

## 📁 **Archivos Esenciales (7 archivos):**

### **Scripts Principales (4 archivos):**
1. **`create_basic_database.sql`** - Script SQL básico para crear la base de datos
2. **`create_db_simple.py`** - Script Python para crear BD y usuario
3. **`create_tables.py`** - Script Python para crear todas las tablas
4. **`insert_test_data_fixed.py`** - Script Python para insertar datos de prueba

### **Scripts de Gestión (3 archivos):**
5. **`setup_complete_database.py`** - Script completo que ejecuta todo el proceso
6. **`test_db_connection.py`** - Probar conexión a la base de datos
7. **`README.md`** - Documentación completa

## 🚀 **Proceso de Configuración**

### **Opción 1: Script Completo (Recomendado)**
```bash
python scripts/setup_complete_database.py
```

### **Opción 2: Scripts Individuales**

#### **Paso 1: Crear Base de Datos y Usuario**
```bash
python scripts/create_db_simple.py
```

#### **Paso 2: Crear Tablas**
```bash
python scripts/create_tables.py
```

#### **Paso 3: Insertar Datos de Prueba**
```bash
python scripts/insert_test_data_fixed.py
```

#### **Paso 4: Verificar Configuración**
```bash
python scripts/test_db_connection.py
```

## 🏗️ **Arquitectura de Base de Datos**

### **Configuración Principal**
- **Motor**: MySQL 8.0+
- **Charset**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Usuario**: bi_user
- **Base de datos**: ganaderia_bi

### **Tablas Principales**
- `marca_ganado_bovino` - Marcas ganaderas (5 registros)
- `logo_marca_bovina` - Logos generados por IA (4 registros)
- `kpi_ganado_bovino` - Métricas y KPIs (1 registro)
- `historial_estado_marca` - Auditoría de cambios (8 registros)
- `dashboard_data` - Datos del dashboard (1 registro)
- `reporte_data` - Reportes generados (2 registros)

## 🔧 **Configuración de Django**

### **settings.py - Configuración de Base de Datos:**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ganaderia_bi",
        "USER": "root",  # Temporalmente usando root
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "sql_mode": "traditional",
            "charset": "utf8mb4",
            "use_unicode": True,
        },
    }
}
```

## ✅ **Verificación de Configuración**

Para verificar que todo funciona correctamente:

```bash
# Probar conexión
python scripts/test_db_connection.py

# Ejecutar servidor Django
python manage.py runserver

# Crear superusuario
python manage.py createsuperuser
```

## 🎯 **Resultado Esperado**

- ✅ Base de datos `ganaderia_bi` creada
- ✅ Usuario `bi_user` con contraseña `password`
- ✅ 6 tablas creadas con estructura completa
- ✅ Datos de prueba insertados
- ✅ Conexión Django funcionando
- ✅ Admin de Django accesible en `/admin/`

## 📝 **Notas Importantes**

1. **Compatibilidad**: Scripts probados con MariaDB/XAMPP en Windows 10
2. **Dependencias**: Requiere `mysql-connector-python` y `PyMySQL`
3. **Permisos**: Necesita acceso root para crear BD y usuario
4. **Backup**: Se recomienda hacer backup antes de ejecutar scripts
5. **Emojis**: Los scripts han sido corregidos para funcionar en Windows

## 🚨 **Solución de Problemas**

### **Error de tabla corrupta:**
Si ves el error "Index for table 'db' is corrupt", es normal en XAMPP y no afecta la funcionalidad.

### **Error de conexión:**
Verifica que XAMPP esté ejecutándose y MySQL esté activo.

---

**🎉 ¡Base de datos lista para usar con Clean Architecture!** 