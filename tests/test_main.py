import pytest
from httpx import AsyncClient
from ..main import  app

# Sample correct Instagram URL
valid_request_payload = {
    "profile_urls": ["https://www.instagram.com/example_user/"]
}

# Sample invalid Instagram URL
invalid_request_payload = {
    "profile_urls": ["https://example.com/not_instagram"]
}

@pytest.mark.asyncio
async def test_valid_predict_request(monkeypatch):
    """Test prediction for valid Instagram URLs"""

    # Mock extractor method
    async def mock_extract_features_from_instagram(urls):
        return [{"username_length": 10, "followers_count": 100, "follows_count": 50}]

    # Mock prediction response
    async def mock_predict_profiles(req):
        return {"predictions": [1], "explanations": ["FAKE"], "probabilities": [0.85]}

    # Monkeypatch internal methods
    from app import extractor
    from app import prediction_client

    monkeypatch.setattr(extractor, "extract_features_from_instagram", mock_extract_features_from_instagram)
    monkeypatch.setattr(prediction_client, "predict_profiles", mock_predict_profiles)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predict", json=valid_request_payload)
    assert response.status_code == 200
    assert "predictions" in response.json()

@pytest.mark.asyncio
async def test_invalid_url_exception():
    """Test invalid Instagram URL raises proper exception"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predict", json=invalid_request_payload)
    assert response.status_code == 400
    assert response.json()["detail"]["message"] == "Invalid Instagram profile URL."

@pytest.mark.asyncio
async def test_unexpected_error(monkeypatch):
    """Test unexpected internal error is caught"""

    async def raise_generic_exception(urls):
        raise Exception("Unexpected failure")

    from app import extractor
    monkeypatch.setattr(extractor, "extract_features_from_instagram", raise_generic_exception)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predict", json=valid_request_payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred while processing profiles."
