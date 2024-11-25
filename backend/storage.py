import json
import os
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

FILE_NAME = "posts.json"
PATH = "backend"
JSON_PATH = os.path.join(PATH, FILE_NAME)


def load_posts() -> List[dict]:
    """
    Load posts from a JSON file.

    Returns:
        List[dict]: A list of posts. If the file doesn't exist or is invalid, returns an empty list.
    """
    if not os.path.exists(JSON_PATH):
        logging.warning(
            f"File {JSON_PATH} not found. Returning an empty list."
        )
        return []

    try:
        with open(JSON_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error while reading {JSON_PATH}: {e}")
        logging.info("Return empty list to POSTS")
        return []
    except IOError as e:
        logging.error(f"IO error while reading {JSON_PATH}: {e}")
        logging.info("Return empty list to POSTS")
        return []


def save_posts(posts: List[dict]) -> None:
    """
    Save posts to a JSON file.

    Args:
        posts (List[dict]): The list of posts to save.
    """
    os.makedirs(PATH, exist_ok=True)  # Ensure the directory exists
    try:
        with open(JSON_PATH, "w") as file:
            json.dump(posts, file, indent=4)
        logging.info(f"Posts successfully saved to {JSON_PATH}.")
    except IOError as e:
        logging.error(f"Error saving posts to {JSON_PATH}: {e}")
