import pytest
from pydantic import ValidationError
from app.api.schemas import CreatePost, GetPost, ListPosts, UpdatePost  # замените your_module на ваш реальный модуль

def test_create_post_valid():
    post = CreatePost(owner_id="123", title="Valid Title", description="Short desc", private=True)
    assert post.owner_id == "123"
    assert post.title == "Valid Title"
    assert post.description == "Short desc"
    assert post.private is True

def test_create_post_invalid_length():
    with pytest.raises(ValidationError):
        CreatePost(owner_id="", title="Valid Title", description="Short desc")
    
    with pytest.raises(ValidationError):
        CreatePost(owner_id="a" * 51, title="Valid Title", description="Short desc")

def test_get_post_valid():
    post = GetPost(post_id="post123", owner_id="owner123")
    assert post.post_id == "post123"
    assert post.owner_id == "owner123"

def test_get_post_invalid():
    with pytest.raises(ValidationError):
        GetPost(post_id="", owner_id="owner123")
    
    with pytest.raises(ValidationError):
        GetPost(post_id="post123", owner_id="a" * 51)

def test_list_posts_valid():
    posts = ListPosts(owner_id="owner123", page=2, per_page=20)
    assert posts.owner_id == "owner123"
    assert posts.page == 2
    assert posts.per_page == 20

def test_list_posts_invalid():
    with pytest.raises(ValidationError):
        ListPosts(owner_id="", page=-1, per_page=0)

def test_update_post_valid():
    post = UpdatePost(title="New Title", description="New Description", private=False)
    assert post.title == "New Title"
    assert post.description == "New Description"
    assert post.private is False

def test_update_post_empty_string():
    post = UpdatePost(title=" ", description="", private=None)
    assert post.title is None
    assert post.description is None
    assert post.private is None