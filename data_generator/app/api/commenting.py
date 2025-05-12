import httpx
import random
from app.models.comment import CommentCreate, generate_random_comment
from app.core.config import MAIN_APP_API_URL
from app.utils.user_store import load_users
from app.api.registration import login_user


def submit_comment(comment: CommentCreate, token: str):
    url = f"{MAIN_APP_API_URL}/posts/create_comment"  # Adjust endpoint if needed
    cookies = {"users_access_token": token}
    data = comment.model_dump()
    try:
        response = httpx.post(url, json=data, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        print(f"Comment creation failed: {exc.response.status_code} - {exc.response.text}")
        return None
    except Exception as exc:
        print(f"Comment creation error: {exc}")
        return None


if __name__ == "__main__":
    users = load_users()
    if not users:
        print("No users found in user store. Please register users first.")
    else:
        user = users[0]
        print(f"Logging in as {user.login}...")
        login_result = login_user(user)
        token = None
        if login_result:
            token = login_result.get('user_access_token') or login_result.get('access_token')
        if not token:
            print("Login failed, cannot submit comment.")
        else:
            # get all posts ids
            url = f"{MAIN_APP_API_URL}/posts/list_posts_ids"
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            post_ids = response.json()
            print(f"Post ids: {post_ids}")

            # get random post id
            post_id = random.choice(post_ids)
            print(f"Post id: {post_id}")

            comment = generate_random_comment(post_id)
            print(f"Submitting comment to post {post_id}: {comment.comment}")
            result = submit_comment(comment, token)
            print("Comment submission result:", result)
