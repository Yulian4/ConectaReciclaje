# Agente Ciudadano

Este agente permite a los ciudadanos gestionar reportes de materiales reciclables a través de una interfaz WebSocket. Utiliza FastAPI, Mirascope con Google Gemini, y MCP (Model Context Protocol) para procesar consultas en lenguaje natural y ejecutar operaciones en la base de datos.

## Requisitos del Sistema

- **Python**: Versión 3.12 (especificado en `.python-version`)
- **Gestor de paquetes**: uv (de Astral, documentación oficial: https://docs.astral.sh/uv/)
- **Dependencias**: Ver `pyproject.toml`

## Instalación y Configuración

### 1. Instalar uv
Si no tienes uv instalado, sigue la documentación oficial: https://docs.astral.sh/uv/getting-started/installation/

### 2. Clonar o navegar al directorio del proyecto
```bash
cd Agentes/ciudadano
```

### 3. Crear y activar entorno virtual
```bash
uv venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 4. Instalar dependencias
```bash
uv pip install -e .
```

### 5. Configurar variables de entorno
Copia el archivo `.env.example` a `.env` y configura las variables necesarias:
- `DB_HOST`: Host de la base de datos MySQL
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_NAME`: Nombre de la base de datos
- `TWILIO_SID`: SID de Twilio para envío de SMS
- `TWILIO_TOKEN`: Token de Twilio
- `TWILIO_PHONE`: Número de teléfono de Twilio

## Ejecución

Para ejecutar el agente, usa el siguiente comando:

```bash
uvicorn --reload client:app --port 8000
```

Esto iniciará el servidor WebSocket en `ws://localhost:8765` y el servidor FastAPI en `http://localhost:8000`.

## Funcionalidades

- **Insertar Reporte**: Crear un nuevo reporte de material reciclable
- **Actualizar Reporte**: Modificar un reporte existente
- **Eliminar Reporte**: Borrar un reporte
- **Consultar Reportes**: Listar reportes de un ciudadano

El agente utiliza Google Gemini para interpretar consultas en lenguaje natural y ejecutar las operaciones correspondientes a través de MCP.

## Estructura del Proyecto

- `client.py`: Cliente WebSocket y lógica de procesamiento con LLM
- `server.py`: Servidor MCP con herramientas para gestión de reportes
- `pyproject.toml`: Configuración del proyecto y dependencias
- `.python-version`: Versión de Python requerida
- `.env.example`: Ejemplo de variables de entorno
