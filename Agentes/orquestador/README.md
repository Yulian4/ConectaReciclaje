# Agente Orquestador

Este agente actúa como un orquestador central que recibe solicitudes desde el backend Java y las dirige a los agentes específicos (ciudadano o reciclador) basándose en el rol del usuario. Utiliza FastAPI, Mirascope con Google Gemini, y MCP para el enrutamiento inteligente de solicitudes.

## Requisitos del Sistema

- **Python**: Versión 3.12 (especificado en `.python-version`)
- **Gestor de paquetes**: uv (de Astral, documentación oficial: https://docs.astral.sh/uv/)
- **Dependencias**: Ver `pyproject.toml`

## Instalación y Configuración

### 1. Instalar uv
Si no tienes uv instalado, sigue la documentación oficial: https://docs.astral.sh/uv/getting-started/installation/

### 2. Clonar o navegar al directorio del proyecto
```bash
cd Agentes/orquestador
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

### 5. Configurar variables de entorno (si es necesario)
El agente puede requerir configuración de variables de entorno para la conexión con otros servicios. Verifica si hay un archivo `.env.example` en el directorio.

## Ejecución

Para ejecutar el agente, usa el siguiente comando:

```bash
uvicorn --reload client:app --port 8000
```

Esto iniciará el servidor FastAPI en `http://localhost:8000` con el endpoint `/transfer` para recibir solicitudes del backend Java.

## Funcionalidades

- **Enrutamiento Inteligente**: Utiliza Google Gemini para determinar el rol del usuario y enrutar la solicitud al agente correspondiente
- **Transferencia a Ciudadano**: Envía solicitudes de usuarios con rol "ciudadano" al agente ciudadano vía WebSocket
- **Transferencia a Reciclador**: Envía solicitudes de usuarios con rol "reciclador" al agente reciclador vía WebSocket
- **Integración con Backend**: Recibe solicitudes POST desde el backend Java en el endpoint `/transfer`

## Arquitectura

El agente consta de dos componentes principales:

1. **Cliente (client.py)**: Servidor FastAPI que recibe solicitudes y utiliza LLM para decidir el enrutamiento
2. **Servidor MCP (server.py)**: Proporciona herramientas MCP para transferir solicitudes vía WebSocket a los agentes específicos

## Endpoints

- `POST /transfer`: Recibe solicitudes con `user_id`, `rol` y `query`, y las enruta al agente correspondiente

## Dependencias Externas

- Agente Ciudadano: Debe estar ejecutándose en `ws://localhost:8765`
- Agente Reciclador: Debe estar ejecutándose en `ws://localhost:8766`

## Estructura del Proyecto

- `client.py`: Servidor FastAPI y lógica de enrutamiento con LLM
- `server.py`: Servidor MCP con herramientas de transferencia WebSocket
- `main.py`: Script básico (no utilizado en la ejecución principal)
- `pyproject.toml`: Configuración del proyecto y dependencias
- `.python-version`: Versión de Python requerida
- `.env.example`: Ejemplo de variables de entorno (si existe)
