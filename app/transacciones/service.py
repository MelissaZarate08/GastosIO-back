from app.database import get_connection

def get_all(usuario_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT id, tipo, monto, categoria, descripcion, fecha
               FROM transacciones
               WHERE usuario_id = %s
               ORDER BY fecha DESC""",
            (usuario_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def create(usuario_id: int, tipo: str, monto: float,
           categoria: str, descripcion: str | None) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """INSERT INTO transacciones (usuario_id, tipo, monto, categoria, descripcion)
               VALUES (%s, %s, %s, %s, %s)""",
            (usuario_id, tipo, float(monto), categoria, descripcion),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, tipo, monto, categoria, descripcion, fecha FROM transacciones WHERE id = %s",
            (new_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def update(transaccion_id: int, usuario_id: int, fields: dict) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Verificar que pertenece al usuario
        cursor.execute(
            "SELECT id FROM transacciones WHERE id = %s AND usuario_id = %s",
            (transaccion_id, usuario_id),
        )
        if not cursor.fetchone():
            raise ValueError("Transacción no encontrada")
        
        updates = ", ".join(f"{k} = %s" for k in fields)
        values = list(fields.values()) + [transaccion_id]
        cursor.execute(f"UPDATE transacciones SET {updates} WHERE id = %s", values)
        conn.commit()
        return {"mensaje": f"Transacción {transaccion_id} actualizada correctamente"}
    finally:
        cursor.close()
        conn.close()

def delete(transaccion_id: int, usuario_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM transacciones WHERE id = %s AND usuario_id = %s",
            (transaccion_id, usuario_id),
        )
        if not cursor.fetchone():
            raise ValueError("Transacción no encontrada")
        cursor.execute("DELETE FROM transacciones WHERE id = %s", (transaccion_id,))
        conn.commit()
        return {"mensaje": f"Transacción {transaccion_id} eliminada"}
    finally:
        cursor.close()
        conn.close()