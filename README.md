# SAP Condiciones de Masa - Modificación (Versión 1.0)

## Descripción
Esta aplicación automatiza modificaciones masivas de condiciones de precios en sistemas SAP utilizando la transacción VK12. Está construida con Python, PySide2 para la interfaz gráfica (GUI), y scripting de SAP GUI para interacciones automatizadas. Permite cargar un archivo Excel con datos de modificación, validar los datos, y ejecutar cambios en masa mientras registra el progreso y errores en la GUI.

**Características principales (Versión 1.0):**
- Interfaz gráfica intuitiva para login en SAP, selección de archivo Excel y ejecución.
- Validación automática de datos en el Excel (flujos, campos obligatorios, formatos).
- Soporte para múltiples tipos de modificaciones masivas (material, grupo de artículos, etc.).
- Registro en tiempo real de errores y progreso en el área de texto de la GUI.
- Manejo básico de errores durante validación y procesamiento.

## Instalación
1. Asegúrate de tener Python 3.8+ instalado (configurado vía `mise.toml`).
2. Instala dependencias: Ejecuta `mise run setup` (instala pywin32, pandas, dotenv, PySide2).
3. Configura el archivo `.env` con credenciales SAP (SYSTEM, MANDT, USER, PASSWD, LANGUAGE).
4. Ejecuta la aplicación: `python main.py`.

**Requisitos del sistema:**
- SAP GUI instalado y configurado.
- Archivo Excel de entrada en formato específico (ver sección de Uso).

## Uso
1. Abre la aplicación (`python main.py`).
2. Haz clic en "Abrir Archivo" para seleccionar un Excel con datos (hoja "vk12").
3. Haz clic en "Login SAP" para iniciar sesión.
4. Haz clic en "Ejecutar" para procesar modificaciones masivas.
5. Revisa el log en el área de texto para errores y progreso.

**Formato del Excel de entrada:**
- Columnas requeridas dependen del `TIPO_MODIFICACION` (ej. MATERIAL, IMPORTE, ORG_VENTA).
- Ejemplo de flujos válidos: `mat_orgvent_candistr`, `orgvent_candistr_gpoart`, etc.
- Archivo de prueba: `test_vk12.xlsx` (incluido en el proyecto).

## Estructura del Proyecto
- `main.py`: Interfaz gráfica principal.
- `sap.py`: Lógica de conexión y login a SAP.
- `sap_vk12_massmod.py`: Implementación de flujos de modificación masiva.
- `validators.py`: Validaciones de datos del Excel.
- `ui_sap.py` / `ui_sap.ui`: Archivos de UI generados por Qt Designer.
- `test_project.py`: Unit tests (agregado en esta versión).

## Pruebas
Ejecuta `pytest test_project.py` para validar funcionalidades. Usa `test_vk12.xlsx` para pruebas integrales.

## Pendientes (Futuras Versiones)
- **Exportar errores a Excel**: Generar un archivo Excel con filas inválidas y razones de error (pendiente por ahora).
- **Ampliar unidades de medida válidas**: Agregar más valores a `VALID_UNIDAD_MEDIDA` en `validators.py` según necesidades.
- **Mejoras en validación de flujo de datos**: Implementar exportación de errores para análisis posterior.
- **Pruebas avanzadas**: Agregar mocks para tests de interacción con SAP GUI.
- **Documentación expandida**: Guías detalladas, diagramas de flujo, y ejemplos de uso.

## Licencia
[Agrega licencia si aplica, ej. MIT].
