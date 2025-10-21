from mcp.server.fastmcp import FastMCP
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ==========================================================
# CONFIGURACIÓN DEL MCP
# ==========================================================

mcp = FastMCP("ReportesMCP")

# ==========================================================
# CONFIGURACIÓN BASE DE DATOS MySQL
# ==========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "conectareciclaje",
}


def get_connection():
    """Crea y retorna una conexión a la base de datos MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("Error al conectar a MySQL:", e)
        return None


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================


def execute_query(query: str, params: tuple = (), fetch: bool = False):
    conn = get_connection()
    if conn is None:
        return {"status": "error", "error": "No se pudo conectar a la base de datos"}
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            conn.close()
            return result
        conn.commit()
        conn.close()
        return {"status": "ok"}
    except Error as e:
        conn.rollback()
        conn.close()
        return {"status": "error", "error": str(e)}


# ==========================================================
# HERRAMIENTAS MCP
# ==========================================================


@mcp.tool()
def insertarReporte(
    id_ciudadano: int, material: str, cantidad: float, descripcion: str
) -> dict:
    """
    Inserta un nuevo reporte en la base de datos MySQL.

    Recibe:
        - id_ciudadano: ID del ciudadano
        - material: nombre de la categoria del material (ej: "Plastico")
        - cantidad: cantidad del material
        - descripcion: descripción del reporte

    Primero consulta el ID del material y luego inserta el reporte.
    """
    # Paso 1: obtener el ID del material
    query_material = "SELECT id_material FROM materiales WHERE categoria = %s"
    material_result = execute_query(query_material, (material,), fetch=True)

    if not material_result:
        return {"status": "error", "error": f"Material '{material}' no encontrado"}

    id_material = material_result[0]["id_material"]

    # Paso 2: insertar el reporte usando el id_material
    query_insert = """
        INSERT INTO reportes (id_ciudadano, id_material, cantidad, descripcion)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(
        query_insert, (id_ciudadano, id_material, cantidad, descripcion)
    )


@mcp.tool()
def actualizarReporte(
    id_reporte: int,
    cantidad: float = None,
    descripcion: str = None,
    material: str = None,
) -> dict:
    """
    Actualiza la cantidad, descripción o material de un reporte existente.
    """
    updates = []
    params = []

    # Actualizar cantidad
    if cantidad is not None:
        updates.append("cantidad = %s")
        params.append(cantidad)

    # Actualizar descripción
    if descripcion is not None:
        updates.append("descripcion = %s")
        params.append(descripcion)

    # Actualizar material por nombre
    if material is not None:
        # Primero obtener id_material
        query_material = "SELECT id_material FROM materiales WHERE categoria = %s"
        material_result = execute_query(query_material, (material,), fetch=True)
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


@mcp.tool()
def eliminarReporte(id_reporte: int) -> dict:
    """
    Elimina un reporte por su ID.
    """
    query = "DELETE FROM reportes WHERE id_reporte = %s"
    return execute_query(query, (id_reporte,))


@mcp.tool()
def consultarReportesPorUsuario(id_ciudadano: int) -> dict:
    """
    Consulta todos los reportes asociados a un ciudadano.
    """
    query = "SELECT * FROM reportes WHERE id_ciudadano = %s ORDER BY fecha_hora DESC"
    result = execute_query(query, (id_ciudadano,), fetch=True)
    return {"status": "ok", "reportes": result}


# ==========================================================
# EJECUCIÓN DEL MCP
# ==========================================================

if __name__ == "__main__":
    mcp.run()
