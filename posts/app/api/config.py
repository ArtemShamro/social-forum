import os
from dataclasses import dataclass

@dataclass
class Config:
     DB_CONFIG = os.getenv('DATABASE_URL')