from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.wrappers import Response
from typing import Optional, Dict, Any
from swagger_ui import SWAGGER_URL, swagger_ui_blueprint
from datetime import datetime


app = Flask(__name__)
CORS(app)

# API Documentation with swagger_ui on api/docs
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# ID and dates are generated automatically when creating or updating post
POST_KEYS = ["title", "content", "author"]
POSTS = [
    {
        "id": 1,
        "title": "First post",
        "content": "This is the first post.",
        "author": "Jane Doe",
        "date_created": "01-01-2024",
        "date_modified": "01-01-2024",
    },
    {
        "id": 2,
        "title": "Second post",
        "content": "This is the second post.",
        "author": "John Doe",
        "date_created": "02-01-2024",
        "date_modified": "02-01-2024",
    },
]


@app.route("/api/posts", methods=["GET"])
def get_posts() -> Response:
    """
    Retrieves all posts.

    Returns:
        Response:
            - 200: JSON list of all posts.
    """

    args = request.args

    if "sort" in args:
        sorting_key = args["sort"]

        if sorting_key not in POST_KEYS:
            return jsonify(
                error=f"'{sorting_key}' is not a valid sorting parameter"
            ), 400  # type: ignore
        
        sorting_direction = args.get("direction", None)
        sorted_posts = get_sorted_posts(sorting_key, sorting_direction)
        return jsonify(sorted_posts)

    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post() -> Response:
    """
    Handles the creation of a new post.

    This endpoint accepts a JSON payload representing a new post, validates the
    data, assigns a unique ID to the post, and appends it to the POSTS list.

    Returns:
        Response:
            - 201: JSON representation of the created post if successful.
            - 400: Error message if the input data is invalid.
    """

    new_post = request.get_json()

    if not new_post or not validate_post_data(new_post):
        return jsonify({"error": "Invalid post data"}), 400  # type: ignore

    # Assign a new ID based on the current maximum
    new_post["id"] = max((post.get("id", 0) for post in POSTS), default=0) + 1

    # Assign a new creation date to post
    new_post["date_created"] = datetime.now().strftime("%Y-%m-%d, %H:%M")

    POSTS.append(new_post)

    return jsonify(new_post), 201  # type: ignore


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id: int) -> Response:
    """
    Deletes a post by its ID.

    This endpoint finds the post with the provided ID in the POSTS list.
    If found, the post is deleted, and a success message is returned.
    If the post is not found, a 404 error is returned.

    Args:
        id (int): The ID of the post to be deleted.

    Returns:
        Response: A JSON response with a success or error message.
            - 200: Post successfully deleted.
            - 404: Post not found.
    """

    # Find post by id
    post = find_post(id)
    if not post:
        return jsonify({"error": f"Post with ID:{id} not Found"}), 404  # type: ignore

    # Remove post
    POSTS.remove(post)

    return jsonify({
        "message": f"Post with id {id} has been deleted successfully."
    }), 200  # type: ignore


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id) -> Response:
    """
    Updates an existing post by its ID.

    Args:
        id (int): The ID of the post to update.

    Returns:
        Response:
            - 200: JSON representation of the updated post if successful.
            - 404: Error message if the post is not found.
            - 400: Error message if the input data is invalid.
    """
    post = find_post(id)
    if not post:
        return jsonify(error=f"Post with ID:{id} not Found"), 404  # type: ignore

    new_data = request.get_json()
    if not has_valid_keys(new_data):
        return jsonify(error="Invalid post data"), 400  # type: ignore

    # Assign a new modification date to post
    new_data["date_modified"] = datetime.now().strftime("%Y-%m-%d, %H:%M")

    post.update(new_data)

    return jsonify(post), 200  # type: ignore


@app.route("/api/search", methods=["GET"])
def search_posts() -> Response:
    """
    Searches for posts based on query parameters.

    Query Parameters:
        - title (str, optional): Search term for the post title.
        - content (str, optional): Search term for the post content.
        - author (str, optional): Search term for the post author.
        - date_created (str, optional): Search term for the post creation date.

    Returns:
        Response:
            - 200: JSON list of matching posts if any found.
            - 400: Error message for invalid search parameters.
            - 404: Error message if no matches are found.
    """
    title = request.args.get("title", None)
    content = request.args.get("content", None)
    author = request.args.get("author", None)
    date = request.args.get("date_created", None)

    if title:
        title_search_results = get_search_results(
            search_item=title, key="title"
        )
        return title_search_results  # type: ignore

    elif content:
        content_search_results = get_search_results(
            search_item=content, key="content"
        )
        return content_search_results  # type: ignore

    elif author:
        author_search_results = get_search_results(
            search_item=author, key="author"
        )
        return author_search_results  # type: ignore

    elif date:
        date_search_results = get_search_results(search_item=date, key="date")
        return date_search_results  # type: ignore

    return jsonify(error="Invalid search parameter"), 400  # type: ignore


def validate_post_data(post: dict) -> bool:
    """Validate that required fields are present in the post data.

    Args:
        post (dict): The post data to validate.

    Returns:
        bool: True if the required fields are present, False otherwise.
    """
    required_fields = set(POST_KEYS)
    return required_fields.issubset(post)


def find_post(id: int) -> Optional[Dict[str, Any]]:
    """
    Finds a post by its ID.

    Args:
        id (int): The ID of the post to find.

    Returns:
        dict or None: The post if found, otherwise None.
    """
    return next((post for post in POSTS if post.get("id") == id), None)


def has_valid_keys(post: dict) -> bool:
    """
    Checks if the provided post data contains only valid keys.

    Args:
        post (dict): The post data to validate.

    Returns:
        bool: True if all keys are valid, False otherwise.
    """
    return next((False for key in post if key not in POST_KEYS), True)


def search_for(search_item: str, key: str) -> list:
    """
    Searches for posts matching the specified key and search term.

    Args:
        search_item (str): The term to search for.
        key (str): The field to search within (e.g., title, content).

    Returns:
        list: A list of matching posts.
        Empty if no posts found.
    """
    return [
        post
        for post in POSTS
        if search_item.lower() in post.get(key, None).lower()
    ]


def get_search_results(search_item: str, key: str) -> Response:
    """
    Retrieves search results for the specified term and key.

    Args:
        search_item (str): The term to search for.
        key (str): The field to search within.

    Returns:
        Response:
            - 200: JSON list of matching posts if found.
            - 404: Error message if no matches are found.
    """
    search_results = search_for(search_item=search_item, key=key)
    if search_results:
        return jsonify(search_results), 200  # type: ignore
    return jsonify(error="Nothing found"), 404  # type: ignore


def get_sorted_posts(key: str, direction: str | None) -> list:
    is_reversed = True if direction == "desc" else False
    return sorted(POSTS, key=lambda item: item[key], reverse=is_reversed)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
