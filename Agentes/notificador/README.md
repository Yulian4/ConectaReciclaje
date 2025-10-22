# Agente Notificador

Este agente es un servicio básico de notificación. Actualmente es un placeholder con funcionalidad mínima.

## Requisitos del Sistema

- **Python**: Versión 3.12 (especificado en `.python-version`)
- **Gestor de paquetes**: uv (de Astral, documentación oficial: https://docs.astral.sh/uv/)

## Instalación y Configuración

### 1. Instalar uv
Si no tienes uv instalado, sigue la documentación oficial: https://docs.astral.sh/uv/getting-started/installation/

### 2. Clonar o navegar al directorio del proyecto
```bash
cd Agentes/notificador
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

## Ejecución

Para ejecutar el agente, usa el siguiente comando:

```bash
uv run main.py
```

Esto ejecutará el script principal que imprime un mensaje de saludo.

## Funcionalidades

Actualmente, el agente solo imprime un mensaje de "Hello from notificador!". Está diseñado para ser expandido con funcionalidades de notificación más avanzadas en el futuro.

## Estructura del Proyecto

- `main.py`: Script principal del agente
- `pyproject.toml`: Configuración del proyecto y dependencias
- `.python-version`: Versión de Python requerida
