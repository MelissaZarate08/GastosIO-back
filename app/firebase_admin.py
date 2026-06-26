import firebase_admin
from firebase_admin import credentials, messaging
import os

_cred_path = os.path.join(os.path.dirname(__file__), "firebase_credentials.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(_cred_path)
    firebase_admin.initialize_app(cred)


def send_remote_wipe(fcm_token: str, target_user_id: int, reason: str) -> str:
    """Envía notificación FCM de remote wipe. Retorna el message_id."""
    message = messaging.Message(
        token=fcm_token,
        data={
            "action": "remote_wipe",
            "target_user_id": str(target_user_id),
            "reason": reason,
        },
        notification=messaging.Notification(
            title="Seguridad",
            body="Se eliminaron tus datos sensibles remotamente",
        ),
    )
    return messaging.send(message)