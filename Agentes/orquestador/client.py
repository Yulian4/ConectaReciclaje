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
    """Herramienta para transferir solicitudes hechas ESPECÍFICAMENTE por un usuario con el rol CIUDADANO."""
    user_id: int
    query: str

    async def call(self) -> dict:
        return {"user_id": self.user_id, "query": self.query}


class TransferRecicladorTool(BaseTool):
    """Herramienta para transferir solicitudes hechas ESPECÍFICAMENTE por un usuario con el rol RECICLADOR."""
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
    Analiza la intención del usuario y decide **estrictamente** qué herramienta ejecutar,
    basándose únicamente en el parámetro 'rol'.

    REGLAS:
    1. Si 'rol' == "CIUDADANO" → usar exclusivamente 'TransferCiudadanoTool'.
    2. Si 'rol' == "RECICLADOR" → usar exclusivamente 'TransferRecicladorTool'.
    3. NO cambiar los valores de ningún parámetro. Pasar exactamente:
        - user_id: el ID del usuario recibido
        - query: el texto de la solicitud recibido
    4. NO generar texto adicional, explicaciones ni comentarios.
    5. El LLM debe devolver únicamente un objeto con la herramienta y sus parámetros listo para ejecutar.


    NOTA: Bajo ninguna circunstancia el LLM debe inventar un ID o modificar la query.
    """

app = FastAPI()

async def process_request(user_id: int, rol: str, query: str):
    try:
        llm_response = await analizar_intencion(user_id, rol, query)
        print("Respuesta del LLM:", llm_response)
        print("Iniciando conexión stdio_client con MCP...")

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Sesión MCP inicializada")

                # 🔹 Validar si el LLM seleccionó una herramienta
                if not getattr(llm_response, "tool", None):
                    print("No se encontró ninguna herramienta seleccionada por el LLM.")
                    return {
                        "status": "warning",
                        "message": (
                            "Aún no tengo la capacidad de ejecutar tu solicitud. "
                            "Estaré aprendiendo nuevas funciones muy pronto 😊"
                        ),
                    }

                tool_call = llm_response.tool.tool_call
                print("Llamando herramienta con argumentos:", tool_call)

                tool_name = TOOL_NAME_APP.get(tool_call.name)
                print("Nombre de la herramienta:", tool_name)

                # 🔹 Validar si la herramienta existe en el registro
                if not tool_name:
                    print("No se encuentra el nombre de la herramienta.")
                    return {
                        "status": "warning",
                        "message": (
                            "No tengo disponible esa funcionalidad todavía. "
                            "Por favor, intenta con otra solicitud o más adelante."
                        ),
                    }

                args = tool_call.args

                print("Ejecutando herramienta y pasando argumentos...")
                result = await session.call_tool(tool_name, arguments=args)
                print("La respuesta fue:", result)

                # 🔹 Manejo de errores del resultado
                if result.isError:
                    print("result.isError:", result.content)
                    return {
                        "status": "error",
                        "message": (
                            "Ocurrió un problema al procesar tu solicitud. "
                            "Por favor, intenta nuevamente más tarde."
                        ),
                    }

                # 🔹 Si hay respuesta estructurada
                elif result.structuredContent:
                    print("result.structuredContent:", result.structuredContent)
                    return {
                        "status": "success",
                        "message": "Solicitud completada con éxito.",
                        "data": result.structuredContent,
                    }

                # 🔹 Si hay contenido plano
                elif result.content:
                    content = result.content
                    if isinstance(content, list) and len(content) > 0 and hasattr(content[0], "text"):
                        try:
                            parsed = json.loads(content[0].text)
                            return {
                                "status": "success",
                                "message": "Solicitud procesada correctamente.",
                                "data": parsed,
                            }
                        except Exception:
                            return {
                                "status": "success",
                                "message": "Solicitud completada.",
                                "data": content[0].text,
                            }
                    else:
                        return {
                            "status": "success",
                            "message": "Solicitud completada.",
                            "data": content,
                        }

                # 🔹 Si no hay respuesta
                else:
                    return {
                        "status": "info",
                        "message": (
                            "No encontré información relevante para tu solicitud. "
                            "¿Podrías intentar reformularla?"
                        ),
                    }

    except Exception as e:
        print(f"\n Error durante el proceso: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": (
                "Hubo un error interno al procesar tu solicitud. "
                "Por favor, intenta nuevamente más tarde."
            ),
            "details": str(e),  # opcional, puedes quitarlo en producción
        }



@app.post("/transfer")
async def transfer_endpoint(body: TransferRequest):
    print("Petición recibida desde backend Java:", body.dict())
    result = await process_request(body.user_id,body.rol,body.query)
    return result
