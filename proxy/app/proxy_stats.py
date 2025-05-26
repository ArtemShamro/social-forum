from app.utils import check_login, check_login_or_zero
from fastapi import Request, APIRouter
import grpc
from google.protobuf.json_format import MessageToJson, MessageToDict
import httpx
from proto import stats_pb2
from proto import stats_pb2_grpc
from proto import posts_pb2
from proto import posts_pb2_grpc
import app.schemas as sc
from app.config import Config
import logging
STATS_GRPC_URL = Config.STATS_GRPC_URL
POSTS_GRPC_URL = Config.POSTS_GRPC_URL
AUTH_URL = Config.AUTH_URL

stats = APIRouter()

logger = logging.getLogger(__name__)


@stats.post("/get_count")
async def get_count(request: Request, payload: sc.GetCountRequest):
    user_id = await check_login(request)

    # print("GET COUNT")
    # print(payload)

    grpc_request = stats_pb2.GetCountRequest(
        post_id=payload.post_id,
        targetType=payload.target_type
    )

    async with grpc.aio.insecure_channel(STATS_GRPC_URL) as channel:
        stub = stats_pb2_grpc.StatsServiceStub(channel)

        try:
            grpc_response = await stub.GetCount(grpc_request)
            return {"counter": grpc_response.counter}
        except grpc.RpcError as e:
            return {"message": e.details()}

@stats.get("/get_post_stats")
async def get_post_stats(request: Request, post_id: int):

    # print("GET POST STATS")
    # print(post_id)

    grpc_request = stats_pb2.GetPostStatsRequest(
        post_id=post_id,
    )

    async with grpc.aio.insecure_channel(STATS_GRPC_URL) as channel:
        stub = stats_pb2_grpc.StatsServiceStub(channel)

        try:
            grpc_response = await stub.GetPostStats(grpc_request)
            result = MessageToDict(message=grpc_response, always_print_fields_with_no_presence=True)
            return result
        except grpc.RpcError as e:
            return {"message": e.details()}

@stats.post("/get_dynamics")
async def get_dynamics(request: Request, payload: sc.GetDynamicsRequest):
    user_id = await check_login(request)

    # print("GET DYNAMICS")
    # print(payload)

    grpc_request = stats_pb2.GetDynamicsRequest(
        post_id=payload.post_id,
        targetType=payload.target_type
    )

    async with grpc.aio.insecure_channel(STATS_GRPC_URL) as channel:
        stub = stats_pb2_grpc.StatsServiceStub(channel)

        try:
            grpc_response = await stub.GetDynamics(grpc_request)
            day_data = [
                {"date": item.date, "value": item.value}
                for item in grpc_response.dayData
            ]
            return {"dayData": day_data}
        except grpc.RpcError as e:
            return {"message": e.details()}


@stats.get("/get_top_posts")
async def get_top_posts(request: Request, target_type: str, limit: int = 10):
    # print("GET TOP POSTS", target_type)
    # print(f"Target Type: {target_type}, Limit: {limit}")

    grpc_request = stats_pb2.GetTopPostsRequest(
        targetType=target_type,
        limit=limit
    )

    async with grpc.aio.insecure_channel(STATS_GRPC_URL) as channel:
        stub = stats_pb2_grpc.StatsServiceStub(channel)

        try:
            grpc_response = await stub.GetTopPosts(grpc_request)
            posts_data = list(grpc_response.items)
            id_to_value = {item.id: item.value for item in posts_data}
            post_ids = list(id_to_value.keys())
            print(f"Proxy stats get top posts: {post_ids}")

            posts_grpc_request = posts_pb2.GetPostsRequest(
                post_ids=post_ids
            )
            # get post info from post service
            async with grpc.aio.insecure_channel(POSTS_GRPC_URL) as posts_channel:
                posts_stub = posts_pb2_grpc.PostsServiceStub(posts_channel)

                try:
                    grpc_response = await posts_stub.GetPosts(posts_grpc_request)
                    posts_info = list(grpc_response.posts)
                    # generate json response
                    response = []
                    for post in posts_info:
                        response.append({
                            "id": post.post_id,
                            "title": post.title,
                            "value": id_to_value[int(post.post_id)]
                        })
                    # print("Proxy stats get top posts response", response)
                    return response
                except grpc.RpcError as e:
                    return {"message": e.details()}
                
        except grpc.RpcError as e:
            return {"message": e.details()}


@stats.get("/get_top_users")
async def get_top_users(request: Request, target_type: str, limit: int = 10):
    # print("GET TOP USERS", target_type)
    # print(f"Target Type: {target_type}, Limit: {limit}")

    grpc_request = stats_pb2.GetTopUsersRequest(
        targetType=target_type,
        limit=limit
    )

    async with grpc.aio.insecure_channel(STATS_GRPC_URL) as channel:
        stub = stats_pb2_grpc.StatsServiceStub(channel)

        try:
            grpc_response = await stub.GetTopUsers(grpc_request)
            users_data = list(grpc_response.items)
            id_to_value = {item.id: item.value for item in users_data}
            user_ids = list(id_to_value.keys())
            # print(f"Proxy stats get top users: {user_ids}")

            # get user info from auth service
            async with httpx.AsyncClient() as client:
                # print("Proxy stats get top users", users_data)
                response = await client.post(
                    f"{AUTH_URL}/get_users",
                    json={"user_ids": user_ids}
                )
                response_data = response.json()
                for item in response_data:
                    item["value"] = id_to_value[item["id"]]
                # print("Proxy stats get top users response", response_data)
                return response_data

        except grpc.RpcError as e:
            return {"message": e.details()}
