from pydantic import BaseModel
from typing import Optional

class FcmTokenRequest(BaseModel):
    fcm_token: str

class RemoteWipeRequest(BaseModel):
    target_user_id: int
    reason: Optional[str] = "Wipe remoto solicitado"