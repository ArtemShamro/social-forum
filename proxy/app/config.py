import os
from dataclasses import dataclass

@dataclass
class Config:
     ENC_DATA = {"secret_key": os.getenv('SECRET_KEY'), 
                "algorithm": os.getenv('ALGORITHM')}
     POSTS_GRPC_URL = os.getenv('POSTS_GRPC_URL')
     AUTH_URL = os.getenv('AUTH_URL')