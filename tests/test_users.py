# ✅ Test Creating a User
def test_create_user(client):
    response = client.post(
        "/users/", json={"name": "Jin Chen", "email": "jinchen@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jin Chen"
    assert data["email"] == "jinchen@example.com"
    assert "id" in data
    assert "created_at" in data


# ❌ Test Creating User with Invalid Email
def test_create_user_invalid_email(client):
    response = client.post(
        "/users/", json={"name": "Test User", "email": "invalid-email"}
    )
    assert response.status_code == 422  # Unprocessable Entity


# ❌ Test Duplicate Email
def test_create_duplicate_email(client):
    client.post("/users/", json={"name": "User1", "email": "duplicate@example.com"})
    response = client.post(
        "/users/", json={"name": "User2", "email": "duplicate@example.com"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# ✅ Test Get User by ID
def test_get_user(client):
    create_response = client.post(
        "/users/", json={"name": "Get User", "email": "getuser@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Get User"


# ❌ Test Get Non-Existent User
def test_get_non_existent_user(client):
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# ✅ Test Update User
def test_update_user(client):
    create_response = client.post(
        "/users/", json={"name": "Old Name", "email": "updateuser@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.put(f"/users/{user_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


# ❌ Test Update User with Existing Email
def test_update_user_existing_email(client):
    client.post("/users/", json={"name": "User1", "email": "email1@example.com"})
    create_response = client.post(
        "/users/", json={"name": "User2", "email": "email2@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.put(f"/users/{user_id}", json={"email": "email1@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already in use"


# ✅ Test Delete User
def test_delete_user(client):
    create_response = client.post(
        "/users/", json={"name": "Delete Me", "email": "deleteme@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

    # Verify user is deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
