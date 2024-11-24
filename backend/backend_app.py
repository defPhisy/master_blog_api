from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.wrappers import Response

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


def validate_post_data(post: dict) -> bool:
    """Validate that required fields are present in the post data.

    Args:
        post (dict): The post data to validate.

    Returns:
        bool: True if the required fields are present, False otherwise.
    """
    required_fields = {"title", "content"}
    return required_fields.issubset(post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
