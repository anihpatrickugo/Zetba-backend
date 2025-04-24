import random
import string

def generate_alphanumeric_code(length=16):
    """
    Generates a random alphanumeric string of the specified length.

    Args:
        length (int, optional): The length of the code to generate. Defaults to 16.

    Returns:
        str: A random alphanumeric string.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

