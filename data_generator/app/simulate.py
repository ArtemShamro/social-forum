import random
import time
from app.utils.user_store import load_users, save_user
from app.api.registration import login_user, register_user, update_user_profile
from app.models.user import generate_random_user
from app.models.post import generate_random_post
from app.api.posting import submit_post
from app.models.comment import generate_random_comment
from app.api.commenting import submit_comment
from app.core.config import MAIN_APP_API_URL
import httpx


def simulate_activity(min_fake_users: int, posts_to_create: int, comments_to_create: int):
    users = load_users()
    # Generate and register missing users
    if len(users) < min_fake_users:
        print(f"Generating {min_fake_users - len(users)} new users...")
        for _ in range(min_fake_users - len(users)):
            user = generate_random_user()
            reg_result = register_user(user)
            if reg_result:
                # Optionally update profile after registration
                login_result = login_user(user)
                token = None
                if login_result:
                    token = login_result.get('user_access_token') or login_result.get('access_token')
                if token:
                    update_user_profile(user, token=token)
                save_user(user)
        users = load_users()

    # Create posts
    for _ in range(posts_to_create):
        user = random.choice(users)
        login_result = login_user(user)
        token = None
        if login_result:
            token = login_result.get('user_access_token') or login_result.get('access_token')
        if not token:
            print(f"Login failed for {user.login}, skipping post.")
            continue
        post = generate_random_post()
        print(f"{user.login} submitting post: {post.title}")
        post_result = submit_post(post, token)
        print("Post submission result:", post_result)
        time.sleep(random.uniform(0.1, 0.2))

    # get post ids from proxy
    url = f"{MAIN_APP_API_URL}/posts/list_posts_ids"
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    post_ids = response.json()
    if not post_ids:
        print("No posts created, skipping comments.")
        return

    # Create comments
    for _ in range(comments_to_create):
        user = random.choice(users)
        login_result = login_user(user)
        token = None
        if login_result:
            token = login_result.get('user_access_token') or login_result.get('access_token')
        if not token:
            print(f"Login failed for {user.login}, skipping comment.")
            continue
        num_posts_to_comment = random.randint(1, min(3, len(post_ids)))
        posts_to_comment = random.sample(post_ids, num_posts_to_comment)
        for post_id in posts_to_comment:
            comment = generate_random_comment(post_id)
            print(f"{user.login} commenting on post {post_id}: {comment.comment}")
            comment_result = submit_comment(comment, token)
            print("Comment submission result:", comment_result)
            time.sleep(random.uniform(0.5, 2.0))


if __name__ == "__main__":
    # Example usage: 5 users, 10 posts, 20 comments
    simulate_activity(min_fake_users=10, posts_to_create=0, comments_to_create=50)
