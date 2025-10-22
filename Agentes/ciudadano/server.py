# ==========================================================
# ReportesMCP - Manejo de reportes y notificaciones SMS
# ==========================================================
from mcp.server.fastmcp import FastMCP
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from twilio.rest import Client
import os

# ==========================================================
# CONFIGURACIÓN DEL MCP
# ==========================================================

mcp = FastMCP("ReportesMCP")

# ==========================================================
# CONEXIÓN BASE DE DATOS MySQL
# ==========================================================

def get_db_connection():
    """Crea y retorna una conexión a la base de datos MySQL usando variables de entorno"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "1234"),
            database=os.getenv("DB_NAME", "conectarecicla")
        )
        return conn
    except Error as e:
        print(" Error al conectar a MySQL:", e)
        return None

# ==========================================================
# CONFIGURACIÓN TWILIO
# ==========================================================

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
print("holaaaa")


client = Client(TWILIO_SID, TWILIO_TOKEN)

# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def execute_query(query: str, params: tuple = (), fetch: bool = False):
    conn = get_db_connection()
    if conn is None:
        return {"status": "error", "error": "No se pudo conectar a la base de datos"}
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "ok"}
    except Error as e:
        conn.rollback()
        conn.close()
        return {"status": "error", "error": str(e)}

def enviar_sms(numero_destino: str, mensaje: str):
    """Envía un SMS usando Twilio"""
    try:
        msg = client.messages.create(
            body=mensaje,
            from_=TWILIO_PHONE,
            to=numero_destino
        )
        return {"status": "ok", "sid": msg.sid}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# ==========================================================
# HERRAMIENTAS MCP
# ==========================================================

@mcp.tool()
def insertarReporte(
    id_ciudadano: int, material: str, cantidad: float, descripcion: str
) -> dict:
    """
    Inserta un nuevo reporte en la base de datos MySQL y notifica
    a los recicladores del mismo barrio mediante SMS.
    """

    # Paso 1: obtener el ID del material
    query_material = "SELECT id_material FROM materiales WHERE categoria = %s"
    material_result = execute_query(query_material, (material,), fetch=True)
    if not material_result:
        return {"status": "error", "error": f"Material '{material}' no encontrado"}
    id_material = material_result[0]["id_material"]

    # Paso 2: insertar el reporte
    query_insert = """
        INSERT INTO reportes (id_ciudadano, id_material, cantidad, descripcion)
        VALUES (%s, %s, %s, %s)
    """
    insert_result = execute_query(
        query_insert, (id_ciudadano, id_material, cantidad, descripcion)
    )
    if insert_result["status"] != "ok":
        return insert_result

    # Paso 3: obtener barrio del ciudadano
    query_ciudadano = """
        SELECT b.nombre AS barrio, u.nombre_completo, u.telefono
        FROM usuarios u
        JOIN direccion d ON u.id_direccion = d.id_direccion
        JOIN barrio b ON d.id_barrio = b.id_barrio
        WHERE u.id_usuario = %s AND u.rol = 'ciudadano'
    """
    ciudadano = execute_query(query_ciudadano, (id_ciudadano,), fetch=True)
    if not ciudadano:
        return {"status": "error", "error": "Ciudadano no encontrado o sin rol válido"}

    barrio = ciudadano[0]["barrio"]
    nombre_ciudadano = ciudadano[0]["nombre_completo"]

    # Paso 4: obtener recicladores del mismo barrio
    query_recicladores = """
        SELECT u.nombre_completo, u.telefono
        FROM usuarios u
        JOIN direccion d ON u.id_direccion = d.id_direccion
        JOIN barrio b ON d.id_barrio = b.id_barrio
        WHERE u.rol = 'reciclador' AND b.nombre = %s
    """
    recicladores = execute_query(query_recicladores, (barrio,), fetch=True)
    if not recicladores:
        return {
            "status": "ok",
            "message": f"Reporte insertado. No hay recicladores en el barrio '{barrio}'.",
        }

    # Paso 5: enviar notificación SMS a cada reciclador
    mensaje = (
        f"♻️ Nuevo reporte en tu zona ({barrio})!\n"
        f"Material: {material}\n"
        f"Cantidad: {cantidad} kg\n"
        f"Ciudadano: {nombre_ciudadano}\n"
        f"Descripción: {descripcion}"
    )

    notificaciones = []
    for rec in recicladores:
        telefono = rec["telefono"]
        print(f"📱 Enviando SMS a reciclador: {rec['nombre_completo']} - Teléfono: {telefono}")
        if telefono:
            resultado_sms = enviar_sms(telefono, mensaje)
            notificaciones.append(
                {
                    "reciclador": rec["nombre_completo"],
                    "telefono": telefono,
                    "resultado": resultado_sms["status"],
                }
            )

    return {
        "status": "ok",
        "message": f"Reporte insertado y notificaciones enviadas a {len(notificaciones)} recicladores.",
        "notificaciones": notificaciones,
    }

@mcp.tool()
def consultarReportesPorUsuario(id_ciudadano: int) -> dict:
    """Consulta todos los reportes asociados a un ciudadano."""
    query = "SELECT * FROM reportes WHERE id_ciudadano = %s ORDER BY fecha_hora DESC"
    result = execute_query(query, (id_ciudadano,), fetch=True)
    return {"status": "ok", "reportes": result}

@mcp.tool()
def eliminarReporte(id_reporte: int) -> dict:
    """Elimina un reporte por su ID."""
    query = "DELETE FROM reportes WHERE id_reporte = %s"
    return execute_query(query, (id_reporte,))

@mcp.tool()
def actualizarReporte(
    id_reporte: int, cantidad: float = None, descripcion: str = None, material: str = None
) -> dict:
    """Actualiza los datos de un reporte."""
    updates, params = [], []

    if cantidad is not None:
        updates.append("cantidad = %s")
        params.append(cantidad)
    if descripcion is not None:
        updates.append("descripcion = %s")
        params.append(descripcion)
    if material is not None:
        material_result = execute_query(
            "SELECT id_material FROM materiales WHERE categoria = %s",
            (material,),
            fetch=True,
        )
        if not material_result:
            return {"status": "error", "error": f"Material '{material}' no encontrado"}
        id_material = material_result[0]["id_material"]
        updates.append("id_material = %s")
        params.append(id_material)

    if not updates:
        return {"status": "error", "error": "No hay campos para actualizar"}

    query = f"UPDATE reportes SET {', '.join(updates)} WHERE id_reporte = %s"
    params.append(id_reporte)
    return execute_query(query, tuple(params))


if __name__ == "__main__":
    print(" Probando conexión a la base de datos...")
    conn = get_db_connection()
    if conn:
        print("Conexión exitosa a MySQL.")
        conn.close()
    else:
        print(" No se pudo conectar a MySQL.")

    print("\n ReportesMCP activo y escuchando...")
    mcp.run()