import os
from dataclasses import dataclass

@dataclass
class Config:
     DB_CONFIG = os.getenv('DATABASE_URL', 'postgresql+asyncpg://posts_db_username:posts_db_password@localhost:13501/posts_db_dev')