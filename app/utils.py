import re
from textblob import TextBlob

def count_digits(text: str) -> int:
    return sum(char.isdigit() for char in text)

def count_word_occurrences(text: str, words: list) -> int:
    return sum(word.lower() in text.lower() for word in words)

def sentiment_score(text: str) -> float:
    return TextBlob(text).sentiment.polarity

def extract_hashtags(text: str) -> int:
    return len(re.findall(r"#\w+", text))

def extract_mentions(text: str) -> int:
    return len(re.findall(r"@\w+", text))

def extract_urls(text: str) -> int:
    return len(re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text))

def extract_external_urls(text: str) -> int:
    return len(re.findall(r"(?i)\b(?:https?|ftp):\/\/[^\s/$.?#].[^\s]*\b", text))


# utils.py

def extract_username_from_url(profile_url: str) -> str:
    """Extracts the username from an Instagram profile URL."""
    if profile_url.startswith("https://www.instagram.com/"):
        # Split the URL by '/' and get the second-to-last element (which is the username)
        username = profile_url.split("/")[-2]
        return username
    else:
        return "unknown_user"  # Return a default value if the URL format is incorrect