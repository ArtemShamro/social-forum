import httpx
from app.models.post import PostCreate, generate_random_post
from app.core.config import MAIN_APP_API_URL
from app.utils.user_store import load_users
from app.api.registration import login_user


def submit_post(post: PostCreate, token: str):
    url = f"{MAIN_APP_API_URL}/posts/create_post"  # Adjust endpoint if needed
    cookies = {"users_access_token": token}
    data = post.model_dump()
    try:
        response = httpx.post(url, json=data, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        print(f"Post creation failed: {exc.response.status_code} - {exc.response.text}")
        return None
    except Exception as exc:
        print(f"Post creation error: {exc}")
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
            print("Login failed, cannot submit post.")
        else:
            post = generate_random_post()
            print(f"Submitting post: {post.title}")
            result = submit_post(post, token)
            print("Post submission result:", result)
