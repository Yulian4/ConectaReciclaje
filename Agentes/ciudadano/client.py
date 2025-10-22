import os
import json
import asyncio
from pydantic import Field,BaseModel
from dotenv import load_dotenv
from mirascope import llm, BaseTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import websockets
load_dotenv()

server_params = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp", "server.py"]  
)


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
    Analiza la consulta (query) en lenguaje natural y decide la operación.

    Ejemplo de salida JSON esperada:
    {{
      "herramienta": "MCP",
      "operacion": "insertar",
      "parametros": {{
        "id_ciudadano": "123",
        "material": "cartón",
        "cantidad": "5 kg",
        "descripcion": "Cajas en la esquina."
      }}
    }}
    """

async def process_request(user_id: int, query: str):
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Sesión MCP inicializada")

                # Paso 1: analizar la query con el LLM
                llm_response = await analizar_query(query)
                print("LLM response:", llm_response)

                if not llm_response.tool:
                    return {"error": "Gemini no identificó herramienta válida"}

                # Extraer tool y argumentos
        
                tool_call = llm_response.tool.tool_call
                tool_name = TOOL_NAME_APP.get(tool_call.name)
                if not tool_name:
                    return {"error": f"Herramienta inesperada: {tool_call.name}"}

                args = tool_call.args
                result = await session.call_tool(tool_name, arguments=args)
                
                if result.isError:
                    print("result.isError:", result.content)
                    return {"error": result.content}

                elif result.structuredContent:
                    print("result.structuredContent:", result.structuredContent)
                    return {"data": result.structuredContent}

                elif result.content:
                    content = result.content
                    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], "text"):
                        try:
                            parsed = json.loads(content[0].text)
                            return parsed
                        except Exception:
                            return {"data": content[0].text}
                    else:
                        return {"data": content}

                else:
                    return {"error": "Respuesta vacía o desconocida"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}



async def handle_websocket_request(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            user_id = data.get("user_id")
            query = data.get("query")
            if not user_id or not query:
                await websocket.send(json.dumps({"error": "Datos incompletos"}))
                continue
            result = await process_request(user_id,query)
            await websocket.send(json.dumps(result))
        except Exception as e:
            print("Cliente desconectado:", e)



WS_PORT=8765

async def start_ws_server():
    print(f"MCP-Complaints activo en ws://localhost:{WS_PORT}")
    async with websockets.serve(handle_websocket_request, "localhost", WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_ws_server())
