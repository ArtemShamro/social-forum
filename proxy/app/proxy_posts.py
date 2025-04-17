from fastapi import Request, Response, APIRouter
import httpx
import grpc
from google.protobuf.json_format import MessageToJson, Parse
import json
from proto import posts_pb2
from proto import posts_pb2_grpc
import app.schemas as sc
from app.config import Config
from app.kafka_producer import KafkaProducer

GRPC_URL = Config.POSTS_GRPC_URL

from app.utils import check_login, grpc_post_responce_to_json, check_login_or_zero

posts = APIRouter()
kafka_producer = KafkaProducer()

@posts.post("/create_post")
async def create_post(request: Request, payload: sc.CreatePostRequest):
    
    user_id = await check_login(request)

    print("CREATE POST")
    print(payload)
    
    grpc_request = posts_pb2.CreatePostRequest(
        owner_id=user_id,
        title=payload.title,
        description=payload.description,
        private=payload.private
    )

    with grpc.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try: 
            grpc_response = stub.CreatePost(grpc_request)
            post = grpc_response.post
            print("POST:: ", post)
            post_json = grpc_post_responce_to_json(post)
            return post_json
        except grpc.RpcError as e:
            print("EXCEPTION LAL : ", e)
            return {'message': e.details()}


@posts.post("/get_post")
async def get_post(request: Request, payload: sc.GetPostRequest):
    
    user_id = await check_login_or_zero(request)

    print("GET POST")
    print(request)
    
    grpc_request = posts_pb2.GetPostRequest(
        owner_id=user_id,
        post_id=payload.post_id
    )

    async with grpc.aio.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = await stub.GetPost(grpc_request)
            post = grpc_response.post
            json_str = MessageToJson(post, always_print_fields_with_no_presence=True)
            json_dict = json.loads(json_str)
            if user_id != 0:
                kafka_producer.send_post_view_event(user_id, json_dict['postId'], json_dict['title'])
            return json_dict
        except grpc.RpcError as e:
            return {'message': e.details()}


@posts.get("/list_posts")
async def list_posts(request: Request, page: int = 1, per_page: int = 10):
    
    user_id = await check_login_or_zero(request)

    print("LIST POSTS")
    print(request)
    
    grpc_request = posts_pb2.ListPostsRequest(
        owner_id=user_id,
        page=page,
        per_page=per_page
    )

    async with grpc.aio.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = await stub.ListPosts(grpc_request)
            posts = grpc_response.posts
            json_str = [MessageToJson(post, always_print_fields_with_no_presence=True) for post in posts]
            json_dict = [json.loads(post) for post in json_str]
            return json_dict
        except grpc.RpcError as e:
            return {'message': e.details()}


@posts.post("/delete_post")
async def delete_post(request: Request, payload: sc.DeletePostRequest):
    
    user_id = await check_login(request)

    print("DELETE POST")
    print(request)

    grpc_request = posts_pb2.DeletePostRequest(
        owner_id=user_id,
        post_id=payload.post_id
    )

    with grpc.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = stub.DeletePost(grpc_request)
            post = grpc_response.post
            json_str = MessageToJson(post, always_print_fields_with_no_presence=True)
            json_dict = json.loads(json_str)
            return json_dict
        
        except grpc.RpcError as e:
            return {'message': e.details()}
        

@posts.post("/update_post")
async def update_post(request: Request, payload: sc.UpdatePostRequest):
    
    user_id = await check_login(request)

    print("UPDATE POST")

    grpc_request = posts_pb2.UpdatePostRequest(
        owner_id=user_id,
        post_id=payload.post_id,
        title=payload.title,
        description=payload.description,
        private=payload.private
    )

    print(grpc_request)

    async with grpc.aio.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = await stub.UpdatePost(grpc_request)
            post = grpc_response.post
            json_str = MessageToJson(post, always_print_fields_with_no_presence=True)
            json_dict = json.loads(json_str)
            return json_dict
        except grpc.RpcError as e:
            return {'message': e.details()}
        

@posts.post("/like_post")
async def like_post(request: Request, post_id: int = 1,):
    
    user_id = await check_login(request)

    print("LIKE POST")
    print("types :", type(post_id), type(user_id))
    grpc_request = posts_pb2.LikePostRequest(
        post_id=post_id,
        user_id=user_id
    )

    async with grpc.aio.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = await stub.LikePost(grpc_request)
            kafka_producer.send_post_like_event(user_id, post_id)
            return {'message': 'Post liked'}
        except grpc.RpcError as e:
            return {'message': e.details()}
        
@posts.post("/create_comment")
async def create_comment(request: Request, payload: sc.CreateCommentRequest):
    
    user_id = await check_login(request)

    print("CREATE COMMENT")
    print(payload)
    
    grpc_request = posts_pb2.CreateCommentRequest(
        post_id=payload.post_id,
        user_id=user_id,
        comment=payload.comment
    )

    with grpc.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = stub.CreateComment(grpc_request)
            kafka_producer.send_post_comment_event(user_id, payload.post_id)
            return {'message': 'Comment created'}
        except grpc.RpcError as e:
            return {'message': e.details()}
        

@posts.get("/list_comments")
async def list_posts(request: Request, post_id: int, page: int = 1, per_page: int = 10):
    
    print("LIST COMMENTS")
    
    grpc_request = posts_pb2.GetPostCommentsRequest(
        post_id=post_id,
        page=page,
        per_page=per_page
    )

    async with grpc.aio.insecure_channel(GRPC_URL) as channel:
        stub = posts_pb2_grpc.PostsServiceStub(channel)
        
        try:
            grpc_response = await stub.GetPostComments(grpc_request)
            comments = grpc_response.comments
            json_str = [MessageToJson(comment, always_print_fields_with_no_presence=True) for comment in comments]
            json_dict = [json.loads(comment) for comment in json_str]
            return json_dict
        except grpc.RpcError as e:
            return {'message': e.details()}