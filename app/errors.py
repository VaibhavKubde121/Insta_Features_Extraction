# app/errors.py

# app/errors.py

ERRORS = {
    "INVALID_URL": {
        "code": 1001,
        "message": "The provided Instagram profile URL is invalid."
    },
    "SCRAPER_FAILED": {
        "code": 1002,
        "message": "Failed to extract data from the Instagram profile."
    },
    "MISSING_FIELDS": {
        "code": 1003,
        "message": "Required profile fields are missing from the request."
    },
    "INTERNAL_ERROR": {
        "code": 1004,
        "message": "An unexpected internal error occurred."
    },
    "PRIVATE_PROFILE": {
        "code": 1005,
        "message": "The Instagram profile is private and cannot be scraped."
    },
    "RATE_LIMITED": {
        "code": 1006,
        "message": "Rate limit exceeded. Please try again later."
    },
    "SCRAPER_TIMEOUT": {
        "code": 1007,
        "message": "The scraper timed out while processing the profile."
    },
    "MALFORMED_RESPONSE": {
        "code": 1008,
        "message": "Received malformed or incomplete data from the scraper."
    },
    "SERVICE_UNAVAILABLE": {
        "code": 1009,
        "message": "The scraping service is temporarily unavailable. Please try again."
    },
    "INVALID_REQUEST_BODY": {
        "code": 1010,
        "message": "The request body format is invalid or missing required structure."
    },
    "UNAUTHORIZED_ACCESS": {
        "code": 1011,
        "message": "Access to service is unauthorized."
    }
}