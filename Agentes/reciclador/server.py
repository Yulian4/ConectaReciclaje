
from mcp.server.fastmcp import FastMCP
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import traceback
from dotenv import load_dotenv
load_dotenv()


mcp = FastMCP("RecicladorMCP")

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
# FUNCIONES AUXILIARES
# ==========================================================
def execute_query(query: str, params: tuple = (), fetch: bool = False):
    """Ejecuta una consulta SQL, permitiendo SELECT o INSERT/UPDATE/DELETE"""
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


@mcp.tool()
def consultar_reportes_cercanos(id_reciclador: int) -> dict:
    """
    Devuelve todos los reportes de ciudadanos que estén en el mismo barrio que el reciclador.
    Excluye los reportes ya asignados.
    """

    sql = """
        SELECT 
            r.id_reporte, 
            r.descripcion, 
            r.cantidad, 
            m.categoria, 
            b.nombre AS barrio, 
            u.nombre_completo AS ciudadano
        FROM reportes r
        JOIN usuarios u ON r.id_ciudadano = u.id_usuario
        JOIN materiales m ON r.id_material = m.id_material
        JOIN direccion d_u ON u.id_direccion = d_u.id_direccion
        JOIN barrio b ON d_u.id_barrio = b.id_barrio
        WHERE b.id_barrio = (
            SELECT d.id_barrio
            FROM usuarios ur
            JOIN direccion d ON ur.id_direccion = d.id_direccion
            WHERE ur.id_usuario = %s
        )
        AND r.id_reporte NOT IN (SELECT id_reporte FROM asignaciones)
    """

    try:
        resultados = execute_query(sql, (id_reciclador,), fetch=True)
        if not resultados:
            return {"status": "ok", "message": "No hay reportes disponibles en tu barrio."}
        return {"status": "ok", "reportes_cercanos": resultados}
    except Exception as e:
        print("Error DB:", traceback.format_exc())
        return {"status": "error", "error": str(e)}


@mcp.tool()
def aceptar_reporte(
    id_reciclador: int,
    id_reporte: int,
    fecha_asignada: str = None,
    hora_asignada: str = None    
) -> dict:
    """
    Permite al reciclador aceptar un reporte y programar cuándo pasará a recogerlo.
    Si no se envían fecha/hora, se usa la fecha y hora actuales.
    """

    if fecha_asignada is None:
        fecha_asignada = datetime.now().strftime("%Y-%m-%d")
    if hora_asignada is None:
        hora_asignada = datetime.now().strftime("%H:%M:%S")

    query_insert = """
        INSERT INTO asignaciones (id_reporte, id_reciclador, fecha_asignada, hora_asignada, estado)
        VALUES (%s, %s, %s, %s, 'pendiente')
    """

    try:
        result = execute_query(query_insert, (id_reporte, id_reciclador, fecha_asignada, hora_asignada))
        if result["status"] == "ok":
            return {
                "status": "ok",
                "mensaje": f"Reporte {id_reporte} asignado exitosamente al reciclador {id_reciclador} para el {fecha_asignada} a las {hora_asignada}."
            }
        else:
            return result
    except Exception as e:
        print("Error DB:", traceback.format_exc())
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    print(" Probando conexión a la base de datos...")
    conn = get_db_connection()
    if conn:
        print(" Conexión exitosa a MySQL.")
        conn.close()
    else:
        print(" No se pudo conectar a MySQL.")

    print("\n RecicladorMCP activo y escuchando...")
    mcp.run()
