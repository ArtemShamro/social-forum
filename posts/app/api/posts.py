import logging
import sys
import grpc
from concurrent import futures
from proto import posts_pb2
from proto import posts_pb2_grpc
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.schemas import *
from app.api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.api.db_manager import PostsDB
from app.api.utils import post_to_grpc

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s - %(levelname)s - %(message)s")


class PostsServicer(posts_pb2_grpc.PostsServiceServicer):
    
    
    async def CreatePost(self, request, context):
        logging.info(f"Received message: {request}")
        
        payload = CreatePost(
            owner_id=request.owner_id,
            title=request.title,
            description=request.description,
            private=request.private
        )

        logging.info(f"Payload: {payload}")
        
        async with get_db() as session:  
            new_post = await PostsDB.add_post(payload, session)
            print("NEW POST::", new_post)
            new_post = post_to_grpc(new_post)

        response = posts_pb2.PostResponse(post=new_post)
        return response


    async def GetPost(self, request, context):
        logging.info(f"Received message: {request}")
        
        payload = GetPost(
            post_id=request.post_id,
            owner_id=request.owner_id
        )
        async with get_db() as session:  
            post = await PostsDB.get_post(payload, session)
            if post is None:
                print("Post not found")
                await context.abort(grpc.StatusCode.NOT_FOUND, f"Post with id {request.post_id} not found")
            if post.private == True and post.owner_id != request.owner_id:
                print(post.owner_id, type(post.owner_id))
                print("You don't have permission to access this post")
                await context.abort(grpc.StatusCode.PERMISSION_DENIED, f"You don't have permission to access this post")
            post = post_to_grpc(post)
            response = posts_pb2.PostResponse(post=post)
            return response


    async def ListPosts(self, request, context):
        logging.info(f"Received message: {request}")
        
        payload = ListPosts(
            owner_id=request.owner_id,
            page=request.page,
            per_page=request.per_page
        )
        async with get_db() as session:  
            posts = await PostsDB.list_posts(payload, session)
            if posts is None:
                print("Posts not found")
                await context.abort(grpc.StatusCode.NOT_FOUND, f"Posts with owner_id {request.owner_id} not found")
            posts = [post_to_grpc(post) for post in posts]
            response = posts_pb2.PostList(posts=posts)
            return response
        

    async def UpdatePost(self, request, context):
        logging.info(f"Received message: {request}")
        
        post = await check_edit_permission(request, context)
        
        payload_update = UpdatePost(
            title=request.title,
            description=request.description,
            private=request.private
        )

        async with get_db() as session:  
            updated_post = await PostsDB.update_post(payload_update,  int(request.post_id), session)
            post = post_to_grpc(updated_post)
            response = posts_pb2.PostResponse(post=post)
            return response


    async def DeletePost(self, request, context):
        logging.info(f"Received message: {request}")
        
        post = await check_edit_permission(request, context)

        async with get_db() as session:  
            post = await PostsDB.delete_post(int(request.post_id), session)
            post = post_to_grpc(post)
            response = posts_pb2.PostResponse(post=post)
            return response



async def check_edit_permission(request, context):
    payload = GetPost(
        post_id=request.post_id,
        owner_id=request.owner_id
    )
    async with get_db() as session:  
        post = await PostsDB.get_post(payload, session)
        if post is None:
            print("Post not found")
            await context.abort(grpc.StatusCode.NOT_FOUND, f"Post with id {request.post_id} not found")
        if post.owner_id != request.owner_id:
            print(post.owner_id, type(post.owner_id))
            print("You don't have permission to access this post")
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, f"You don't have permission to access this post")
        return post


@asynccontextmanager
async def serve(app: FastAPI):
    logging.info('Starting gRPC server...')
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostsServiceServicer_to_server(PostsServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    try:
        yield
    finally:
        logging.info('Shutting down gRPC server...')
        await server.stop(grace=2)