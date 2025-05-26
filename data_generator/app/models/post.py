from pydantic import BaseModel
from faker import Faker
import random


class PostCreate(BaseModel):
    title: str
    description: str
    private: bool


fake = Faker()


def generate_random_post():
    title = fake.sentence(nb_words=6)
    description = fake.text(max_nb_chars=50)
    private = False  # random.choice([True, False])
    return PostCreate(title=title, description=description, private=private)
