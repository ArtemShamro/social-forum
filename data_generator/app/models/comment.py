from pydantic import BaseModel
from faker import Faker


class CommentCreate(BaseModel):
    post_id: int
    comment: str


fake = Faker()


def generate_random_comment(post_id: int) -> CommentCreate:
    comment = fake.sentence(nb_words=12)
    return CommentCreate(post_id=post_id, comment=comment)
