from pydantic import BaseModel
from typing import List, Optional


class ProfileListRequest(BaseModel):
    signature: str
    profile_urls: List[str]

class FeatureResponse(BaseModel):
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

class ProfileRequest(FeatureResponse):
    pass

class BulkProfilesRequest(BaseModel):
    profiles: List[ProfileRequest]

class PredictionResponseItem(BaseModel):
    profile_ref: str
    prediction: str

class PredictionResponse(BaseModel):
    status: str
    code: int
    message: str
    data: List[PredictionResponseItem]


class ErrorResponse(BaseModel):
    code: int
    message: str
    details: Optional[str] = None