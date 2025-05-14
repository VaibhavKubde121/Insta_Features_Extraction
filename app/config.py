APIFY_API_TOKEN = "apify_api_h7wOyPLQdNgvQmPToqXuYRkLgH6Aql4xTZYq"
# APIFY_TASK_ID = "xusQysP0PLJAhRmOc"
# APIFY_ACTOR_ID = "drobnikj/instagram-profile-scraper"
SUSPICIOUS_WORDS = [
    "free", "offer", "click", "win", "visit", "bit.ly", "giveaway", "contest", "exclusive",
    "limited", "now", "hurry", "urgent", "subscribe", "get", "only", "bonus", "easy", "fast",
    "prize", "guaranteed", "instant", "secret", "reward", "claim"
]

SPAM_WORDS = [
    "buy", "discount", "promo", "sale", "deal", "shop", "order", "cash", "code", "coupon",
    "bargain", "lowest", "percent off", "clearance", "limited-time", "save big", "cheap",
    "best price", "hot deal", "special offer", "shopping", "purchase"
]


PREDICTION_SERVICE_URL = "http://127.0.0.1:8000"

# My service API_SECRET_KEY
API_SECRET_KEY = "B7@dX#9Kq$1m^tFW!ZgL&pY82uERvj5A*hM0Nc!xoQz4UVSfb6TLkwC#iD3n%JM"


PLATFORM_REF_INSTAGRAM="instagram"

# uvicorn main:app --reload --port 8001