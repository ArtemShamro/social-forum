import os
from dataclasses import dataclass

@dataclass
class Config:
     ENC_DATA = {"secret_key": "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt", 
                "algorithm": "HS256"}
     DB_CONFIG = os.getenv('DATABASE_URL')