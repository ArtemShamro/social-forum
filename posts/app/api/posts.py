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

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s - %(levelname)s - %(message)s")

class PostsServicer(posts_pb2_grpc.PostsServiceServicer):
    async def CreatePost(self, request, context):
        # print(f"Received post creation request: {request}")
        logging.info(f"Received message: {request}")
        payload = PostCreate(
            owner_id=request.owner_id,
            title=request.title,
            description=request.description,
            private=request.private
        )
        logging.info(f"Payload: {payload}")
        
        async with get_db() as session:  # Используем сессию в контексте
            await PostsDB.add_post(payload, session)

        # Эмулируем создание поста
        response = posts_pb2.PostCreateResponse(order_status="SUCCESS")

        return response

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
        server.stop(grace=2)