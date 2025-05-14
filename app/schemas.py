from pydantic import BaseModel
from typing import List, Optional


# Schema for a single profile's features (with username and platform_ref included)
class FeatureRequest(BaseModel):
    username: str
    platform_ref: str
    username_length: int
    num_digits_in_username: int
    profile_has_picture: int
    profile_has_bio: int
    bio_word_count: int
    spam_word_count: int
    suspicious_words_in_bio: int
    bio_sentiment_score: float
    followers_count: int
    follows_count: int
    friend_follower_ratio: float
    posts_count: int
    activity_score: float
    joined_recently: int
    is_verified: int


# Request schema for bulk prediction
class BulkProfilesRequest(BaseModel):
    profiles: List[FeatureRequest]


# Response schema for each prediction result
class PredictionResult(BaseModel):
    username: str
    prediction: str  # "Fake" or "Legit"


# Success Response Schema
class SuccessResponse(BaseModel):
    status: str = "success"
    code: int
    message: str
    data: List[PredictionResult]


# Error Response Schema
class ErrorResponse(BaseModel):
    status: str = "error"
    code: int
    message: str
    details: Optional[str] = None


# Request schema to handle the incoming list of Instagram URLs and signature
class ProfileListRequest(BaseModel):
    signature: str
    profile_urls: List[str]