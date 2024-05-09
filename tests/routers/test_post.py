import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient) -> dict:
    return await create_post("Test Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict) -> dict:
    return await create_comment("Test Comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    """Test simple base case of creating a post"""
    body = "Test Post"

    response = await async_client.post("/post", json={"body": body})
    response_dict = response.json()

    assert response.status_code == 201
    assert response_dict["id"] == 0
    assert response_dict["body"] == body


@pytest.mark.anyio
async def test_create_post_no_body(async_client: AsyncClient):
    """Test behavior when body isn't provided when trying to create a post"""
    response = await async_client.post("/post", json={})
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "body"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }


@pytest.mark.anyio
async def test_create_post_extra_keys(async_client: AsyncClient):
    """Test behavior when creating a post and sending extra keys in the post request"""
    body = "Test Post"

    response = await async_client.post(
        "/post", json={"body": body, "extra_key": "extra_value"}
    )
    response_dict = response.json()

    assert response.status_code == 201
    assert response_dict["id"] == 0
    assert response_dict["body"] == body


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    """Test fetching all posts"""
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post):
    """Test simple case of creating a comment"""
    body = "Test Comment"
    response = await async_client.post(
        "/comment",
        json={
            "body": body,
            "post_id": created_post["id"],
        },
    )

    response_dict = response.json()
    assert response.status_code == 201
    assert response_dict["id"] == 0
    assert response_dict["body"] == body
    assert response_dict["post_id"] == created_post["id"]


@pytest.mark.anyio
async def test_get_comments_on_post(async_client: AsyncClient, created_comment: dict):
    """Test getting all comments on a post"""
    response = await async_client.get(f"/post/{created_comment['post_id']}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_post_no_comments(
    async_client: AsyncClient, created_post: dict
):
    """Test getting all comments on a post, no comments exist"""
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_comment: dict, created_post: dict
):
    """Test simple case of getting a post with all it's comments"""
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment],
    }


@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_comment: dict, created_post: dict
):
    """Test case of getting a post with all it's comments when it doesn't exist"""
    response = await async_client.get("/post/2")

    assert response.status_code == 404
    assert response.json() == {"detail": "Post 2 not found."}
