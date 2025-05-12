import random
import string

def generate_random_string(min_length=0, max_length=50):
    length = random.randint(min_length, max_length)
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string