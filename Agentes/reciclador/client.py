import os
import json
import asyncio
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from mirascope import llm, BaseTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import websockets

load_dotenv()

server_params = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp", "server.py"]  # tu MCP servidor con herramientas
)


class ConsultarReportesCercanosTool(BaseTool):
    """
    Herramienta para que el reciclador consulte los reportes
    cercanos disponibles en su mismo barrio.
    """
    id_reciclador: int = Field(..., description="Identificador único del reciclador")

    async def call(self) -> dict:
        return {"id_reciclador": self.id_reciclador}

class AceptarReporteTool(BaseTool):
    id_reciclador: int = Field(..., description="Identificador del reciclador")
    id_reporte: int = Field(..., description="ID del reporte a aceptar")
    id_direccion: int | None = Field(None, description="Dirección asociada (opcional)")
    observacion: str | None = Field(None, description="Nota u observación del reciclador")

    async def call(self) -> dict:
        return {
            "id_reciclador": self.id_reciclador,
            "id_reporte": self.id_reporte,
            "id_direccion": self.id_direccion,
            "observacion": self.observacion
        }

TOOL_NAME_APP = {
    "ConsultarReportesCercanosTool": "consultar_reportes_cercanos",
    "AceptarReporteTool": "aceptar_reporte"
}


@llm.call(
    "google",
    model="gemini-2.5-pro",
    tools=[ConsultarReportesCercanosTool, AceptarReporteTool]
)
async def analizar_query(query: str):
    """
    Analiza el mensaje natural del reciclador y determina si
    debe consultar reportes cercanos o aceptar uno.

    Ejemplos:
    - “Quiero ver los reportes disponibles cerca de mí”
      → ConsultarReportesCercanosTool

    - “Acepto el reporte número 4”
      → AceptarReporteTool
    """
    pass



async def process_request(user_id: int, query: str):
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Sesión MCP inicializada")

                # 1️⃣ Analizar la intención del reciclador
                llm_response = await analizar_query(query)
                print("LLM response:", llm_response)

                if not llm_response.tool:
                    return {"error": "Gemini no identificó ninguna herramienta válida."}


                tool_call = llm_response.tool.tool_call
                tool_name = TOOL_NAME_APP.get(tool_call.name)

                if not tool_name:
                    return {"error": f"Herramienta inesperada: {tool_call.name}"}

                args = tool_call.args
                print(f"Llamando herramienta {tool_name} con args:", args)


                result = await session.call_tool(tool_name, arguments=args)

                if result.isError:
                    return {"error": result.content}

                elif result.structuredContent:
                    return {"data": result.structuredContent}

                elif result.content:
                    content = result.content
                    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], "text"):
                        try:
                            return json.loads(content[0].text)
                        except Exception:
                            return {"data": content[0].text}
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
                await websocket.send(json.dumps({"error": "Faltan datos en la solicitud"}))
                continue

            result = await process_request(user_id, query)
            await websocket.send(json.dumps(result))
        except Exception as e:
            print("Error procesando mensaje WebSocket:", e)


WS_PORT = 8768


async def start_ws_server():
    print(f"RecicladorMCP-Cliente activo en ws://localhost:{WS_PORT}")
    async with websockets.serve(handle_websocket_request, "localhost", WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_ws_server())
