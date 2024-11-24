from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.wrappers import Response
from typing import Optional, Dict, Any

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/api/posts", methods=["GET"])
def get_posts() -> Response:
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


def validate_post_data(post: dict) -> bool:
    """Validate that required fields are present in the post data.

    Args:
        post (dict): The post data to validate.

    Returns:
        bool: True if the required fields are present, False otherwise.
    """
    required_fields = {"title", "content"}
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
