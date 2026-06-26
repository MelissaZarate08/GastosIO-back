from app.database import get_connection
from app.firebase_admin import send_remote_wipe
from datetime import datetime

def save_fcm_token(usuario_id: int, fcm_token: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE usuarios SET fcm_token = %s WHERE id = %s",
            (fcm_token, usuario_id),
        )
        conn.commit()
        return {"mensaje": "FCM token registrado correctamente"}
    finally:
        cursor.close()
        conn.close()

def get_fcm_token(usuario_id: int) -> str | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT fcm_token FROM usuarios WHERE id = %s", (usuario_id,)
        )
        row = cursor.fetchone()
        return row["fcm_token"] if row else None
    finally:
        cursor.close()
        conn.close()

def request_remote_wipe(requester_id: int, target_user_id: int, reason: str) -> dict:
    if requester_id != target_user_id:
        raise PermissionError("No puedes solicitar wipe de otra cuenta")

    fcm_token = get_fcm_token(target_user_id)
    if not fcm_token:
        raise ValueError("No hay FCM token registrado para este usuario")

    message_id = send_remote_wipe(fcm_token, target_user_id, reason)

    return {
        "message": "Notificación de remote wipe enviada",
        "message_id": message_id,
        "sent_at": datetime.utcnow().isoformat() + "Z",
    }