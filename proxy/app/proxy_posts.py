from fastapi import Request, Response, APIRouter
import httpx
import grpc
from proto import posts_pb2
from proto import posts_pb2_grpc
from app.schemas import *
from app.config import Config
GRPC_URL = Config.POSTS_GRPC_URL

from app.utils import check_login

posts = APIRouter()

@posts.post("/create_post")
async def create_post(response: Response, request: Request, payload: PostCreateRequest):
    
    user_id = await check_login(request)

    print("CREATE POST")
    print(payload)
    grpc_request = posts_pb2.PostCreateRequest(
        owner_id=str(user_id),
        title=payload.title,
        description=payload.description,
        private=payload.private
    )

    with grpc.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        grpc_response = stub.CreatePost(grpc_request)

    return {'message': grpc_response.order_status}

# @posts.post("/delete_post")
# async def delete_post(response: Response, request: PostDeleteRequest):
    
#     user_id = check_login(request)

#     print("DELETE POST")
#     print(request)
#     grpc_request = posts_pb2.PostDeleteRequest(
#         owner_id=user_id,
#         post_id=request.post_id
#     )

#     with grpc.insecure_channel(GRPC_URL) as channel:
#         stub = posts_pb2_grpc.PostsServiceStub(channel)
#         grpc_response = stub.DeletePost(grpc_request)

#     return {'message': grpc_response.order_status}

# @posts.post("/update_post")
# async def update_post(response: Response, request: PostUpdateRequest):
    
#     user_id = check_login(request)

#     print("UPDATE POST")
#     print(request)
#     grpc_request = posts_pb2.PostUpdateRequest(
#         owner_id=user_id,
#         post_id=request.post_id,
#         title=request.title,
#         description=request.description,
#         private=request.private
#     )

#     with grpc.insecure_channel(GRPC_URL) as channel:
#         stub = posts_pb2_grpc.PostsServiceStub(channel)
#         grpc_response = stub.UpdatePost(grpc_request)

#     return {'message': grpc_response.order_status}

# @posts.get("/get_post_by_id")
# async def get_post_by_id(response: Response, request: PostGetRequest):
    
#     user_id = check_login(request)

#     print("GET POST BY ID")
#     print(post_id)
#     grpc_request = posts_pb2.PostGetRequest(
#         post_id=post_id
#     )

#     with grpc.insecure_channel(GRPC_URL) as channel:
#         stub = posts_pb2_grpc.PostsServiceStub(channel)
#         grpc_response = stub.GetPostById(grpc_request)

#     return {'message': grpc_response.order_status}