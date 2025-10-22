from mcp.server.fastmcp import FastMCP
import asyncio
import websockets
import json

mcp = FastMCP("TransferMCP")

URL_CIUDADANO = "ws://localhost:8765/ciudadano"
URL_RECICLADOR = "ws://localhost:8766/reciclador"

# =========================
# FUNCIÓN AUXILIAR
# =========================
async def send_websocket_message(url: str, data: dict):
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps(data))
            response = await websocket.recv()
            return json.loads(response)
    except Exception as e:
        return {"error": str(e)}

# =========================
# TOOLS ASÍNCRONAS
# =========================
@mcp.tool()
async def transferrequestCiudadano(id_usuario: int, query: str) -> dict:
    """Envía una solicitud al canal WebSocket de ciudadanos"""
    data = {"id_usuario": id_usuario, "query": query}
    response = await send_websocket_message(URL_CIUDADANO, data)
    return response


@mcp.tool()
async def transferrequestReciclador(id_usuario: int, query: str) -> dict:
    """Envía una solicitud al canal WebSocket de recicladores"""
    data = {"id_usuario": id_usuario, "query": query}
    response = await send_websocket_message(URL_RECICLADOR, data)
    return response

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    mcp.run()
