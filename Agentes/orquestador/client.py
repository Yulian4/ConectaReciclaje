import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from dotenv import load_dotenv
from fastapi import FastAPI
from mirascope import llm, BaseTool
from pydantic import BaseModel, Field
import json

load_dotenv()


server_params = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp", "server.py"]
)


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

class TransferRequest(BaseModel):
    user_id: int 
    rol: str 
    query: str 


TOOL_NAME_APP = {
    "TransferCiudadanoTool": "transferrequestCiudadano",
    "TransferRecicladorTool": "transferrequestReciclador"
}

@llm.call(
    "google",
    model="gemini-2.5-pro",
    tools=[TransferCiudadanoTool, TransferRecicladorTool]
)
async def analizar_intencion(user_id: int, rol: str, query: str):
    """
    **INSTRUCCIÓN PRINCIPAL:
    - Si el usuario solo saluda o hace un comentario trivial (ej: 'hola'), 
      devuelve un mensaje de saludo directamente sin ejecutar ninguna herramienta.
    **pero si es diferente a un saludo debe ejecutar una sola herramienta**.
    Bajo NINGUNA circunstancia debes generar texto de respuesta, comentarios o explicaciones.
    Solo debes devolver el objeto de la herramienta a ejecutar.

    **REGLAS DE EJECUCIÓN:**

    1.  **Si `rol` es "CIUDADANO" (o "ciudadano"):**
        Ejecuta la herramienta `TransferCiudadanoTool`, pasando los parámetros:
        -   `user_id=user_id`
        -   `query=query`
        
        *Ejemplo de ejecución deseada:* `TransferCiudadanoTool(user_id=user_id, query=query)`

    2.  **Si `rol` es "RECICLADOR" (o "reciclador"):**
        Ejecuta la herramienta `TransferRecicladorTool`, pasando los parámetros:
        -   `user_id=user_id`
        -   `query=query`
        
        *Ejemplo de ejecución deseada:* `TransferRecicladorTool(user_id=user_id, query=query)`
    """

app = FastAPI()

async def process_request(user_id: int, rol: str, query: str):
    try:
        print("Iniciando conexión stdio_client con MCP...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Sesión MCP inicializada")

                # Paso 1: usar el LLM para decidir qué herramienta ejecutar
                llm_response = await analizar_intencion(user_id, rol, query)
                print("Respuesta del LLM:", llm_response)

                if not getattr(llm_response, "tool", None):
                    print("No se encontroninguna herramienta")
                    return {"error": "LLM no seleccionó ninguna herramienta"}

        
                tool_call = llm_response.tool.tool_call
                print("llamando herramienta con argumentos:", tool_call)

                tool_name = TOOL_NAME_APP.get(tool_call.name)
                print("nombre de la herramienta:", tool_name)
                
                if not tool_name:
                    print("no se encuentra el nombre de la herramineta")
                    return {"error": f"Herramienta desconocida: {tool_call.name}"}
                
                args = tool_call.args
                print("Ejecutando herramienta y pasando argumento")
                result = await session.call_tool(tool_name, arguments=args)
                print("La respuesta fue:", result)

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
        print(f"\n Error durante el proceso: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}



@app.post("/transfer")
async def transfer_endpoint(body: TransferRequest):
    print("Petición recibida desde backend Java:", body.dict())
    result = await process_request(body.user_id,body.rol,body.query)
    return result
