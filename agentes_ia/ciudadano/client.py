import os
import json
import asyncio
from mirascope import llm, BaseTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ==========================================================
# CONFIGURACIÓN INICIAL
# ==========================================================

os.environ["MIRASCOPE_DOCSTRING_PROMPT_TEMPLATE"] = "ENABLED"
os.environ["MIRASCOPE_DEBUG"] = "1"

# Conexión al MCP ReportesMCP por stdio
server_params = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp", "reportes_mcp.py"]  # tu MCP con herramientas de reportes
)

# ==========================================================
# TOOLS LLM PARA DESGLOSAR LA QUERY
# ==========================================================

class InsertarReporteTool(BaseTool):
    """
    Herramienta para REGISTRAR o CREAR un nuevo reporte de material reciclable. 
    Se usa cuando el usuario quiere 'hacer', 'insertar', 'registrar' o 'crear' un reporte.
    """
    id_ciudadano: int
    material: str
    cantidad: float
    descripcion: str

    async def call(self) -> dict:
        return {
            "id_ciudadano": self.id_ciudadano,
            "material": self.material,
            "cantidad": self.cantidad,
            "descripcion": self.descripcion
        }


class ActualizarReporteTool(BaseTool):
    """
    Herramienta para MODIFICAR o EDITAR un reporte de material existente. 
    Requiere el 'id_reporte' y al menos uno de los campos opcionales ('cantidad', 'descripcion', 'material') para ser cambiado.
    Se usa cuando el usuario quiere 'cambiar', 'modificar', 'editar' o 'corregir' un reporte específico.
    """
    id_reporte: int
    cantidad: float = None
    descripcion: str = None
    material: str = None

    async def call(self) -> dict:
        return {
            "id_reporte": self.id_reporte,
            "cantidad": self.cantidad,
            "descripcion": self.descripcion,
            "material": self.material
        }


class EliminarReporteTool(BaseTool):
    """
    Herramienta para ELIMINAR o CANCELAR un reporte de material existente. 
    Requiere el 'id_reporte' del informe a borrar. 
    Se usa cuando el usuario quiere 'borrar', 'eliminar', 'quitar' o 'cancelar' un reporte.
    """
    id_reporte: int

    async def call(self) -> dict:
        return {"id_reporte": self.id_reporte}


class ConsultarReportesTool(BaseTool):
    """
    Herramienta para RECUPERAR o LISTAR los reportes asociados a un ciudadano. 
    Requiere el 'id_ciudadano' para buscar sus reportes. 
    Se usa cuando el usuario quiere 'ver', 'listar', 'mostrar', 'revisar' o 'consultar' sus reportes.
    """
    id_ciudadano: int

    async def call(self) -> dict:
        return {"id_ciudadano": self.id_ciudadano}


# Mapeo de tools LLM → herramientas MCP
TOOL_NAME_APP = {
    "InsertarReporteTool": "insertarReporte",
    "ActualizarReporteTool": "actualizarReporte",
    "EliminarReporteTool": "eliminarReporte",
    "ConsultarReportesTool": "consultarReportesPorUsuario"
}


# ==========================================================
# LLM PARA DESGLOSAR LA QUERY
# ==========================================================

@llm.call(
    "google",
    model="gemini-2.5-pro",
    tools=[InsertarReporteTool, ActualizarReporteTool, EliminarReporteTool, ConsultarReportesTool]
)
async def analizar_query(query: str):
    """
    Analiza la consulta (query) en lenguaje natural de un usuario y decide:

    1. Clasifica la intención de la operación: 'insertar', 'actualizar', 'eliminar', o 'consultar'.
    2. Extrae SOLAMENTE los parámetros necesarios para la operación identificada:
        - id_ciudadano
        - id_reporte (usado para UPDATE, DELETE, y a veces CONSULTA específica)
        - material (nombre)
        - cantidad
        - descripcion
    3. Devuelve un objeto JSON con la 'operacion' y el diccionario de 'parametros' extraídos,
       listo para llamar a la herramienta 'MCP'.

    Ejemplo de Salida JSON esperada:
    {
      "herramienta": "MCP",
      "operacion": "insertar",
      "parametros": {
        "id_ciudadano": "123",
        "material": "cartón",
        "cantidad": "5 kg",
        "descripcion": "Cajas en la esquina."
      }
    }
    """


# ==========================================================
# FUNCIÓN CENTRAL DE PROCESAMIENTO
# ==========================================================

async def process_request(payload: dict):
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Sesión MCP inicializada")

                # Paso 1: analizar la query con el LLM
                llm_response = await analizar_query(payload["query"])
                print("LLM response:", llm_response)

                if not getattr(llm_response, "tool", None):
                    return {"error": "LLM no identificó ninguna herramienta"}

                # Extraer tool y argumentos
                tool_name = llm_response.tool.tool_name
                tool_args = llm_response.tool.tool_call.args
                print(f"Herramienta seleccionada: {tool_name} → args: {tool_args}")

                if tool_name not in TOOL_NAME_APP:
                    return {"error": f"Herramienta desconocida: {tool_name}"}

                # Paso 2: llamar a la herramienta MCP correspondiente
                result = await session.call_tool(
                    TOOL_NAME_APP[tool_name],
                    arguments=tool_args
                )
                print("Resultado MCP:", result)
                return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


# ==========================================================
# EJEMPLO DE USO CON WebSocket
# ==========================================================

async def handle_websocket_request(websocket, path):
    async for message in websocket:
        try:
            payload = json.loads(message)
            result = await process_request(payload)
            await websocket.send(json.dumps(result))
        except Exception as e:
            await websocket.send(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    import websockets

    async def main():
        start_server = await websockets.serve(handle_websocket_request, "localhost", 8765)
        print("Cliente MCP escuchando por WebSocket en ws://localhost:8765")
        await start_server.wait_closed()  # Mantener el servidor corriendo

    asyncio.run(main())
