# Masterblog

## Description

A web application that allows users to manage posts through a RESTful API built with Flask. The backend provides endpoints for creating, reading, updating, deleting, and searching posts. The frontend serves a simple interface to display the posts and interact with the backend. The application also includes an interactive API documentation through Swagger UI.

## Features

- **Backend API:**
  - **Create Post:** Add a new post with a title, content, and author.
  - **Retrieve Posts:** Fetch all posts with optional sorting by title, content, author, or date.
  - **Update Post:** Modify the title, content, or author of an existing post.
  - **Delete Post:** Remove a post by its ID.
  - **Search Posts:** Search for posts based on title, content, author, or creation date.
  - **Swagger UI:** Interactive API documentation available at `/api/docs`.
- **Frontend Interface:**
  - Displays posts fetched from the backend.
  - Simple interface that communicates with the backend API to show posts.

## Technologies Used

- **Backend:**
  - Flask for API development
  - Flask-CORS for handling cross-origin requests
  - Swagger UI for API documentation
- **Frontend:**
  - Flask for rendering the homepage and serving HTML content
  - Javascript for client side rendering

## API Endpoints

### `GET /api/posts`

Retrieves all posts. Optionally, posts can be sorted by title, content, author, or creation date using query parameters like `?sort=title&direction=asc`.

### `POST /api/posts`

Creates a new post with the provided title, content, and author. Returns the created post in the response.

### `DELETE /api/posts/<id>`

Deletes a post with the given ID. Returns a success message if successful.

### `PUT /api/posts/<id>`

Updates the post with the given ID. Requires the post ID and updated data in the request body.

### `GET /api/search`

Searches for posts based on query parameters like `title`, `content`, `author`, or `date_created`. Example: `/api/search?title=mysearch`.

## Setup

### Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/defphisy/master_blog_api.git
```

2. Navigate to the project directory:

```bash
cd master_blog_api
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the backend Flask app:

```bash
python backend/backend_app.py
```

- The API will be available at http://127.0.0.1:5002.
- Access the interactive API documentation at http://127.0.0.1:5002/api/docs.

5. Run the frontend Flask app:

```bash
python frontend/frontend_app.py
```

- The frontend will be available at http://127.0.0.1:5001.
