from proto import posts_pb2


def post_to_grpc(post):
    """Преобразует SQLAlchemy-модель в gRPC-сообщение."""
    return posts_pb2.Post(
        post_id=str(post.id),
        owner_id=post.owner_id,
        title=post.title,
        description=post.description,
        private=post.private,
        created_at=post.created_at.isoformat() if post.created_at else "",
        updated_at=post.updated_at.isoformat() if post.updated_at else "",
    )


def comment_to_grpc(comment):
    """Преобразует SQLAlchemy-модель в gRPC-сообщение."""
    return posts_pb2.Comment(
        comment_id=comment.id,
        post_id=comment.post_id,
        user_id=comment.owner_id,
        comment=comment.comment,
        created_at=comment.created_at.isoformat() if comment.created_at else "",
    )
