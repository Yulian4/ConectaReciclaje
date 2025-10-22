import os, ssl, certifi

# Forzar el contexto SSL a usar los certificados válidos del paquete certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
ssl._create_default_https_context = ssl.create_default_context
import json
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import httpx
from mirascope import llm, BaseTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ==========================================================
# CONFIGURACIÓN INICIAL
# ==========================================================

load_dotenv()

os.environ["MIRASCOPE_DOCSTRING_PROMPT_TEMPLATE"] = "ENABLED"
os.environ["MIRASCOPE_DEBUG"] = "1"

# Conexión al servidor MCP (usando uv run --with mcp server.py)
server_params = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp", "server.py"]
)

# ==========================================================
# APP FASTAPI
# ==========================================================

app = FastAPI(title="MCP-Transfer-Client")

# ==========================================================
# MODELOS DE DATOS
# ==========================================================

class TransferRequest(BaseModel):
    user_id: int = Field(..., description="ID del usuario que hace la solicitud")
    rol: str = Field(..., description="Rol del usuario (ciudadano o reciclador)")
    query: str = Field(..., description="Texto o instrucción enviada por el usuario")

# No necesitamos TransferResponse aquí, ya que el Java espera un String JSON
# Pero si quieres mantenerlo, podrías incluirlo igual

# ==========================================================
# TOOLS DEL LLM
# ==========================================================

class TransferCiudadanoTool(BaseTool):
    """Herramienta para transferir solicitud al ciudadano"""
    user_id: int
    query: str

    async def call(self) -> dict:
        return {"user_id": self.user_id, "query": self.query}


class TransferRecicladorTool(BaseTool):
    """Herramienta para transferir solicitud al reciclador"""
    user_id: int
    query: str

    async def call(self) -> dict:
        return {"user_id": self.user_id, "query": self.query}


# ==========================================================
# MAPEADOR DE HERRAMIENTAS
# ==========================================================

TOOL_NAME_APP = {
    "TransferCiudadanoTool": "transferrequestCiudadano",
    "TransferRecicladorTool": "transferrequestReciclador"
}

# ==========================================================
# LLM PARA ANALIZAR ROL
# ==========================================================

@llm.call(
    "google",
    model="gemini-2.5-pro",
    tools=[TransferCiudadanoTool, TransferRecicladorTool]
)
async def analizar_rol(user_id: int, rol: str, query: str):
    """
Tu única tarea es **elegir y ejecutar una herramienta**, sin escribir texto adicional.

- Si el rol es "ciudadano" o "CIUDADANO", llama a TransferCiudadanoTool con exactamente estos argumentos:
  user_id = <user_id proporcionado> y query = <query proporcionada>.
- Si el rol es "reciclador" o "RECICLADOR", llama a TransferRecicladorTool con exactamente estos argumentos:
  user_id = <user_id proporcionado> y query = <query proporcionada>.

No inventes, alteres ni reformules los argumentos.
Usa exactamente los valores recibidos.
"""


# ==========================================================
# FUNCIÓN CENTRAL DE PROCESAMIENTO
# ==========================================================

async def process_request(data: TransferRequest):
    try:
        print("Iniciando conexión stdio_client con MCP...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Sesión MCP inicializada")

                # Paso 1: usar el LLM para decidir qué herramienta ejecutar
                llm_response = await analizar_rol(data.user_id, data.rol, data.query)
                print("Respuesta del LLM:", llm_response)

                if not getattr(llm_response, "tool", None):
                    return {"error": "LLM no seleccionó ninguna herramienta"}

                # ===============================
                # 🔒 Forzar los valores originales del request
                # ===============================
                if hasattr(llm_response.tool, "args"):
                    llm_response.tool.args["user_id"] = data.user_id
                    llm_response.tool.args["query"] = data.query

                # Extraer tool y argumentos (ya corregidos)
                tool_name = getattr(llm_response.tool, "_name", None)
                tool_args = getattr(llm_response.tool, "args", None)
                print(f"Herramienta elegida: {tool_name} → args: {tool_args}")
                # Validar y ejecutar herramienta MCP correspondiente
                if tool_name not in TOOL_NAME_APP:
                    return {"error": f"Herramienta desconocida: {tool_name}"}

                result = await session.call_tool(
                    TOOL_NAME_APP[tool_name],
                    arguments={
                        "id_usuario": tool_args["user_id"],
                        "query": tool_args["query"]
                    }
                )
                print("Respuesta MCP:", result)
                return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


# ==========================================================
# ENDPOINT FASTAPI (versión adaptada al estilo Java)
# ==========================================================

@app.post("/transfer")
async def transfer_endpoint(body: TransferRequest):
    print("Petición recibida desde backend Java:", body.dict())
    result = await process_request(body)
    return result
