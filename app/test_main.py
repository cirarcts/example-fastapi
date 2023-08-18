from fastapi.testclient import TestClient
from main import app, my_posts, Post

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_posts():
    response = client.get("/posts")
    assert response.status_code == 200
    assert "data" in response.json()


def test_create_post():
    post = {
        "title": "Test Post",
        "content": "This is a test post."
    }
    response = client.post("/posts", json=post)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["title"] == post["title"]
    assert data["data"]["content"] == post["content"]


def test_get_post_not_found():
    response = client.get("/posts/9999")  # Assuming 9999 doesn't exist.
    assert response.status_code == 404


def test_update_post():
    # Create a post first
    post_data = {
        "title": "Test Update Post",
        "content": "This is a test post for updating."
    }
    response_create = client.post("/posts", json=post_data)
    created_id = response_create.json()["data"]["id"]

    # Update the post
    updated_data = {
        "title": "Updated Post",
        "content": "This is the updated content."
    }
    response = client.put(f"/posts/{created_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == updated_data["title"]
    assert data["data"]["content"] == updated_data["content"]


def test_delete_post():
    # Create a post first
    post_data = {
        "title": "Test Delete Post",
        "content": "This is a test post for deletion."
    }
    response_create = client.post("/posts", json=post_data)
    created_id = response_create.json()["data"]["id"]

    # Delete the post
    response = client.delete(f"/posts/{created_id}")
    assert response.status_code == 204

    # Check if the post was deleted
    response_get = client.get(f"/posts/{created_id}")
    assert response_get.status_code == 404
