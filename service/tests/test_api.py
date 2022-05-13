import pytest
from bson import ObjectId
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_comments_default(client: AsyncClient, fill_mock_data, mock_data):
    response = await client.get("/comments/default")
    assert response.status_code == 200
    response_data = response.json()
    response_data["items"] = [
        {**item, "_id": ObjectId(item["_id"])} for item in response_data["items"]
    ]
    assert response_data == {"page": 1, "size": 50, "total": 3, "items": mock_data}


@pytest.mark.asyncio
async def test_comments_limit_offset(client: AsyncClient, fill_mock_data, mock_data):
    response = await client.get("/comments/limit-offset")
    assert response.status_code == 200
    response_data = response.json()
    response_data["items"] = [
        {**item, "_id": ObjectId(item["_id"])} for item in response_data["items"]
    ]
    assert response_data == {"limit": 50, "offset": 0, "total": 3, "items": mock_data}
