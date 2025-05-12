from app.utils import check_login, grpc_post_responce_to_json, check_login_or_zero
from fastapi import Request, Response, APIRouter, HTTPException, status
from google.protobuf.json_format import MessageToJson, Parse
from app.config import Config
GRPC_URL = Config.POSTS_GRPC_URL


utils = APIRouter()


@utils.get("/get_user")
async def get_user(request: Request):
    user_id = await check_login_or_zero(request)
    if user_id == "0":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user_id
