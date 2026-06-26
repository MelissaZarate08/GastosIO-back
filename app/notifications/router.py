from fastapi import APIRouter, HTTPException, Depends, status
from .schemas import FcmTokenRequest, RemoteWipeRequest
from . import service
from app.dependencies import get_current_user_id

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notificaciones"],
    dependencies=[Depends(get_current_user_id)],
)

@router.post("/fcm-token")
def register_fcm_token(
    body: FcmTokenRequest,
    usuario_id: int = Depends(get_current_user_id),
):
    return service.save_fcm_token(usuario_id, body.fcm_token)


@router.post("/request-remote-wipe")
def request_remote_wipe(
    body: RemoteWipeRequest,
    usuario_id: int = Depends(get_current_user_id),
):
    try:
        return service.request_remote_wipe(usuario_id, body.target_user_id, body.reason)
    except PermissionError as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(e))
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))