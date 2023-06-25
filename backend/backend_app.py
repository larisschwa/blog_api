from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Get the sort and direction query parameters
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    # Validate the sort and direction values
    if sort and sort not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field. "
                                 "Expected 'title' or 'content'."}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort direction. "
                                 "Expected 'asc' or 'desc'."}), 400

    # Create a copy of the original posts list
    sorted_posts = POSTS[:]

    # Sort the posts based on the provided parameters
    if sort:
        sorted_posts.sort(key=lambda post: post[sort],
                          reverse=(direction == 'desc'))

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"error": "Invalid request. Expected JSON data."}), 400

    # Get the title and content from the request body
    title = request.json.get('title')
    content = request.json.get('content')

    # Check if title and content are provided
    if not title or not content:
        return jsonify({"error": "Title and content are required."}), 400

    # Generate a new unique ID for the new post
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    # Create a new post dictionary
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    # Add the new post to the list of posts
    POSTS.append(new_post)

    # Return the new post as the response
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Find the post with the given id
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {post_id} "
                                       f"has been deleted successfully."}), 200

    # If the post is not found, return an error response
    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"error": "Invalid request. Expected JSON data."}), 400

    # Find the post with the given id
    for post in POSTS:
        if post['id'] == post_id:
            # Get the new title and content from the request body (if provided)
            new_title = request.json.get('title', post['title'])
            new_content = request.json.get('content', post['content'])

            # Update the post with the new values
            post['title'] = new_title
            post['content'] = new_content

            # Return the updated post as the response
            return jsonify(post), 200

    # If the post is not found, return an error response
    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    # Get the title and content query parameters
    title = request.args.get('title')
    content = request.args.get('content')

    # Filter the posts based on the search terms
    filtered_posts = []
    for post in POSTS:
        if (title and title.lower() in post['title'].lower()) or \
                (content and content.lower() in post['content'].lower()):
            filtered_posts.append(post)

    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
