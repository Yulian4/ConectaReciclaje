# Agente Reciclador

Este agente permite a los recicladores consultar reportes de materiales reciclables disponibles en su barrio y aceptar asignaciones de recogida. Utiliza FastAPI, Mirascope con Google Gemini, y MCP (Model Context Protocol) para procesar consultas en lenguaje natural y ejecutar operaciones en la base de datos.

## Requisitos del Sistema

- **Python**: Versión 3.12 (especificado en `.python-version`)
- **Gestor de paquetes**: uv (de Astral, documentación oficial: https://docs.astral.sh/uv/)
- **Dependencias**: Ver `pyproject.toml`

## Instalación y Configuración

### 1. Instalar uv
Si no tienes uv instalado, sigue la documentación oficial: https://docs.astral.sh/uv/getting-started/installation/

### 2. Clonar o navegar al directorio del proyecto
```bash
cd Agentes/reciclador
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

## Ejecución

Para ejecutar el agente, usa el siguiente comando:

```bash
uvicorn --reload client:app --port 8000
```

Esto iniciará el servidor WebSocket en `ws://localhost:8766` y el servidor FastAPI en `http://localhost:8000`.

## Funcionalidades

- **Consultar Reportes Cercanos**: Permite a los recicladores ver reportes disponibles en su mismo barrio que no han sido asignados aún
- **Aceptar Reportes**: Los recicladores pueden aceptar reportes específicos y programar la fecha/hora de recogida

El agente utiliza Google Gemini para interpretar consultas en lenguaje natural y ejecutar las operaciones correspondientes a través de MCP.

## Estructura del Proyecto

- `client.py`: Cliente WebSocket y lógica de procesamiento con LLM
- `server.py`: Servidor MCP con herramientas para gestión de reportes y asignaciones
- `pyproject.toml`: Configuración del proyecto y dependencias
- `.python-version`: Versión de Python requerida
- `.env.example`: Ejemplo de variables de entorno
