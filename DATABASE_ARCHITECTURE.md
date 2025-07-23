# 🗄️ Arquitectura de Base de Datos - GanaderiaBi

## 📋 **Descripción General**

Este documento describe la arquitectura de base de datos del sistema **GanaderiaBi**, implementada siguiendo los principios de **Clean Architecture** y optimizada para el manejo de datos ganaderos.

## 🏗️ **Estructura de Base de Datos**

### **Configuración Principal**
- **Motor**: MySQL 8.0+
- **Charset**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Usuario**: bi_user
- **Base de datos**: ganaderia_bi

### **Tablas Principales**

#### 1. **marca_ganado_bovino** - Marcas Ganaderas
```sql
CREATE TABLE marca_ganado_bovino (
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
);
```

**Campos Clave:**
- `numero_marca`: Identificador único de la marca
- `estado`: Estado del procesamiento (PENDIENTE, EN_PROCESO, APROBADO, RECHAZADO)
- `raza_bovino`: Tipo de raza (NELORE, CRIOLLO, HOLSTEIN, etc.)
- `proposito_ganado`: Propósito (CARNE, LECHE, DOBLE_PROPOSITO, REPRODUCCION)

#### 2. **logo_marca_bovina** - Logos Generados por IA
```sql
CREATE TABLE logo_marca_bovina (
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
);
```

**Campos Clave:**
- `marca_id`: Referencia a la marca
- `exito`: Indica si la generación fue exitosa
- `modelo_ia_usado`: Modelo de IA utilizado (GPT-4, DALL-E-3, etc.)
- `calidad_logo`: Calidad del logo generado

#### 3. **kpi_ganado_bovino** - Métricas y KPIs
```sql
CREATE TABLE kpi_ganado_bovino (
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
);
```

#### 4. **historial_estado_marca** - Auditoría de Cambios
```sql
CREATE TABLE historial_estado_marca (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    marca_id BIGINT NOT NULL,
    estado_anterior VARCHAR(50) NULL,
    estado_nuevo VARCHAR(50) NOT NULL,
    fecha_cambio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_responsable VARCHAR(100) NOT NULL,
    observaciones_cambio TEXT NULL,
    FOREIGN KEY (marca_id) REFERENCES marca_ganado_bovino(id) ON DELETE CASCADE
);
```

#### 5. **dashboard_data** - Datos del Dashboard
```sql
CREATE TABLE dashboard_data (
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
);
```

#### 6. **reporte_data** - Reportes Generados
```sql
CREATE TABLE reporte_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_reporte VARCHAR(50) NOT NULL,
    periodo_inicio DATE NOT NULL,
    periodo_fin DATE NOT NULL,
    formato VARCHAR(20) NOT NULL DEFAULT 'json',
    datos JSON NOT NULL,
    usuario_generador VARCHAR(100) NULL
);
```

## 🔗 **Relaciones entre Tablas**

```
marca_ganado_bovino (1) ←→ (N) logo_marca_bovina
marca_ganado_bovino (1) ←→ (N) historial_estado_marca
```

## 📊 **Vistas Útiles**

### 1. **v_marcas_pendientes** - Marcas Pendientes
```sql
CREATE VIEW v_marcas_pendientes AS
SELECT 
    numero_marca,
    nombre_productor,
    departamento,
    raza_bovino,
    proposito_ganado,
    cantidad_cabezas,
    fecha_registro,
    DATEDIFF(CURRENT_DATE, fecha_registro) as dias_pendiente
FROM marca_ganado_bovino 
WHERE estado = 'PENDIENTE'
ORDER BY fecha_registro ASC;
```

### 2. **v_estadisticas_departamento** - Estadísticas por Departamento
```sql
CREATE VIEW v_estadisticas_departamento AS
SELECT 
    departamento,
    COUNT(*) as total_marcas,
    SUM(cantidad_cabezas) as total_cabezas,
    AVG(cantidad_cabezas) as promedio_cabezas,
    SUM(CASE WHEN estado = 'APROBADO' THEN 1 ELSE 0 END) as marcas_aprobadas,
    SUM(CASE WHEN estado = 'RECHAZADO' THEN 1 ELSE 0 END) as marcas_rechazadas
FROM marca_ganado_bovino 
GROUP BY departamento
ORDER BY total_marcas DESC;
```

### 3. **v_rendimiento_logos** - Rendimiento de Logos
```sql
CREATE VIEW v_rendimiento_logos AS
SELECT 
    modelo_ia_usado,
    COUNT(*) as total_generados,
    SUM(CASE WHEN exito = 1 THEN 1 ELSE 0 END) as exitosos,
    AVG(tiempo_generacion_segundos) as tiempo_promedio,
    AVG(CASE WHEN exito = 1 THEN tiempo_generacion_segundos END) as tiempo_exitosos
FROM logo_marca_bovina 
GROUP BY modelo_ia_usado
ORDER BY total_generados DESC;
```

## ⚡ **Procedimientos Almacenados**

### 1. **sp_calcular_kpis_mensual** - Calcular KPIs
```sql
DELIMITER //
CREATE PROCEDURE sp_calcular_kpis_mensual(IN p_fecha DATE)
BEGIN
    DECLARE v_marcas_registradas INT;
    DECLARE v_tiempo_promedio DECIMAL(10,2);
    DECLARE v_porcentaje_aprobacion DECIMAL(5,2);
    DECLARE v_ingresos_mes DECIMAL(15,2);
    
    -- Calcular métricas
    SELECT 
        COUNT(*),
        AVG(tiempo_procesamiento_horas),
        (SUM(CASE WHEN estado = 'APROBADO' THEN 1 ELSE 0 END) / COUNT(*)) * 100,
        SUM(monto_certificacion)
    INTO v_marcas_registradas, v_tiempo_promedio, v_porcentaje_aprobacion, v_ingresos_mes
    FROM marca_ganado_bovino 
    WHERE DATE_FORMAT(fecha_registro, '%Y-%m') = DATE_FORMAT(p_fecha, '%Y-%m');
    
    -- Insertar o actualizar KPI
    INSERT INTO kpi_ganado_bovino (
        fecha, marcas_registradas_mes, tiempo_promedio_procesamiento, 
        porcentaje_aprobacion, ingresos_mes
    ) VALUES (
        p_fecha, v_marcas_registradas, v_tiempo_promedio, 
        v_porcentaje_aprobacion, v_ingresos_mes
    ) ON DUPLICATE KEY UPDATE
        marcas_registradas_mes = v_marcas_registradas,
        tiempo_promedio_procesamiento = v_tiempo_promedio,
        porcentaje_aprobacion = v_porcentaje_aprobacion,
        ingresos_mes = v_ingresos_mes;
END //
DELIMITER ;
```

### 2. **sp_limpiar_datos_antiguos** - Limpiar Datos Antiguos
```sql
DELIMITER //
CREATE PROCEDURE sp_limpiar_datos_antiguos(IN p_dias INT)
BEGIN
    DELETE FROM historial_estado_marca 
    WHERE fecha_cambio < DATE_SUB(CURRENT_DATE, INTERVAL p_dias DAY);
    
    DELETE FROM reporte_data 
    WHERE fecha_generacion < DATE_SUB(CURRENT_DATE, INTERVAL p_dias DAY);
    
    DELETE FROM dashboard_data 
    WHERE fecha_actualizacion < DATE_SUB(CURRENT_DATE, INTERVAL p_dias DAY);
END //
DELIMITER ;
```

## 🔄 **Triggers Automáticos**

### 1. **tr_actualizar_dashboard_marca** - Actualizar Dashboard
```sql
DELIMITER //
CREATE TRIGGER tr_actualizar_dashboard_marca
AFTER UPDATE ON marca_ganado_bovino
FOR EACH ROW
BEGIN
    UPDATE dashboard_data 
    SET 
        marcas_pendientes = (SELECT COUNT(*) FROM marca_ganado_bovino WHERE estado = 'PENDIENTE'),
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id = (SELECT MAX(id) FROM dashboard_data);
END //
DELIMITER ;
```

### 2. **tr_registrar_cambio_estado** - Registrar Cambios
```sql
DELIMITER //
CREATE TRIGGER tr_registrar_cambio_estado
AFTER UPDATE ON marca_ganado_bovino
FOR EACH ROW
BEGIN
    IF OLD.estado != NEW.estado THEN
        INSERT INTO historial_estado_marca (
            marca_id, estado_anterior, estado_nuevo, 
            usuario_responsable, observaciones_cambio
        ) VALUES (
            NEW.id, OLD.estado, NEW.estado, 
            'sistema', CONCAT('Cambio automático de ', OLD.estado, ' a ', NEW.estado)
        );
    END IF;
END //
DELIMITER ;
```

## 📈 **Índices de Optimización**

### **Índices Principales**
```sql
-- Marcas
CREATE INDEX idx_marca_estado_fecha ON marca_ganado_bovino(estado, fecha_registro);
CREATE INDEX idx_marca_departamento_estado ON marca_ganado_bovino(departamento, estado);
CREATE INDEX idx_marca_numero ON marca_ganado_bovino(numero_marca);

-- Logos
CREATE INDEX idx_logo_fecha_exito ON logo_marca_bovina(fecha_generacion, exito);
CREATE INDEX idx_logo_marca_id ON logo_marca_bovina(marca_id);

-- Historial
CREATE INDEX idx_historial_marca_fecha ON historial_estado_marca(marca_id, fecha_cambio);
CREATE INDEX idx_historial_usuario ON historial_estado_marca(usuario_responsable);

-- KPIs
CREATE INDEX idx_kpi_fecha ON kpi_ganado_bovino(fecha);

-- Dashboard
CREATE INDEX idx_dashboard_fecha ON dashboard_data(fecha_actualizacion);

-- Reportes
CREATE INDEX idx_reporte_tipo_fecha ON reporte_data(tipo_reporte, fecha_generacion);
```

## 🚀 **Comandos de Configuración**

### **1. Configurar Base de Datos**
```bash
# Ejecutar script de configuración
python scripts/setup_database.py

# O usar Makefile
make db-setup
```

### **2. Probar Conexión**
```bash
# Probar conexión
make db-test

# O manualmente
python -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='bi_user', password='password', database='ganaderia_bi'); print('✅ Conexión exitosa')"
```

### **3. Ejecutar Migraciones**
```bash
# Ejecutar migraciones de Django
make db-migrate

# O manualmente
python manage.py migrate
```

### **4. Crear Superusuario**
```bash
# Crear superusuario
make db-superuser

# O manualmente
python manage.py createsuperuser
```

## 📊 **Datos de Prueba**

El script incluye datos de prueba para:
- **5 marcas** con diferentes estados
- **4 logos** generados por IA
- **1 KPI mensual** con métricas
- **10 registros de historial** de cambios
- **1 registro de dashboard** con métricas actuales
- **2 reportes** de ejemplo

## 🔧 **Configuración de Django**

### **settings.py - Configuración de Base de Datos**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ganaderia_bi',
        'USER': 'bi_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## ✅ **Estado de Implementación**

- ✅ **Estructura de tablas**: Completada
- ✅ **Relaciones**: Implementadas
- ✅ **Vistas**: Creadas
- ✅ **Procedimientos**: Implementados
- ✅ **Triggers**: Configurados
- ✅ **Índices**: Optimizados
- ✅ **Datos de prueba**: Incluidos
- ✅ **Scripts de configuración**: Creados

## 🎯 **Beneficios de la Arquitectura**

1. **📈 Escalabilidad**: Estructura optimizada para grandes volúmenes
2. **🔍 Auditoría**: Trazabilidad completa de cambios
3. **⚡ Rendimiento**: Índices optimizados para consultas frecuentes
4. **🛡️ Integridad**: Constraints y foreign keys
5. **📊 Analytics**: Vistas y procedimientos para análisis
6. **🔄 Automatización**: Triggers para actualizaciones automáticas

## 📝 **Próximos Pasos**

1. **Configurar base de datos**: `make db-setup`
2. **Probar conexión**: `make db-test`
3. **Ejecutar migraciones**: `make db-migrate`
4. **Crear superusuario**: `make db-superuser`
5. **Iniciar servidor**: `make run`

---

**🎉 ¡Base de datos lista para usar con Clean Architecture!** 