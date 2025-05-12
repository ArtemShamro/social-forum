import os
from dataclasses import dataclass

@dataclass
class Config:
     ENC_DATA = {"secret_key": os.getenv('SECRET_KEY'), 
                "algorithm": os.getenv('ALGORITHM')}
     DB_CONFIG = os.getenv('DATABASE_URL')