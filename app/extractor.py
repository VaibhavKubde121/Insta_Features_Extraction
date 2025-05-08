# extractor.py
from apify_client import ApifyClient
import logging
from fastapi import HTTPException
from app.config import APIFY_API_TOKEN, SPAM_WORDS, SUSPICIOUS_WORDS
from app.errors import ERRORS
from app.exceptions import GenericInternalException
from app.utils import *

logging.basicConfig(level=logging.INFO)

async def extract_features_from_instagram(profile_urls: list) -> list:
    """
    Extract features for a list of Instagram profile URLs by running the Apify actor via SDK.
    """

    try:
        # Initialize the Apify client
        client = ApifyClient(APIFY_API_TOKEN)

        # Prepare the actor input
        run_input = {
            "directUrls": profile_urls,
            "resultsType": "details"  # This tells Apify to return profile-level data
        }

        # Run the Apify actor and wait for it to finish
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)

        # Fetch results from dataset
        scraped_data = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    except GenericInternalException as e:
        raise e

    except Exception as e:
        logging.error(f"Apify client error: {str(e)}")
        raise GenericInternalException(
            code=ERRORS["INTERNAL_ERROR"]["code"],
            message=ERRORS["INTERNAL_ERROR"]["message"],
            details="Failed during profile extraction."
        )



    features_list = []
    for profile_data in scraped_data:
        bio = profile_data.get("biography", "")
        followers = profile_data.get("followersCount", 0)
        follows = profile_data.get("followsCount", 1)
        posts = profile_data.get("postsCount", 0)
        highlight_reels = profile_data.get("highlightReelCount", 0)

        features = {
            "username_length": len(profile_data.get("username", "")),
            "num_digits_in_username": count_digits(profile_data.get("username", "")),
            "profile_has_picture": int(bool(profile_data.get("profilePicUrlHD"))),
            "profile_has_bio": int(bool(bio.strip())),
            "bio_word_count": len(bio.split()),
            "spam_word_count": count_word_occurrences(bio, SPAM_WORDS),
            "suspicious_words_in_bio": count_word_occurrences(bio, SUSPICIOUS_WORDS),
            "bio_sentiment_score": sentiment_score(bio),
            "followers_count": followers,
            "follows_count": follows,
            "friend_follower_ratio": round(follows / (followers + 1e-5), 2),
            "posts_count": posts,
            "activity_score": round((posts + highlight_reels) / (followers + 1), 2),
            "joined_recently": int(profile_data.get("joinedRecently", False)),
            "is_verified": int(profile_data.get("verified", False)),
        }

        features_list.append(features)

    print("Feature List" , features_list)
    return features_list
