from dbm import error

from fastapi import FastAPI, HTTPException

from app.auth import is_authorized
from app.errors import ERRORS
from app.exception_handler import invalid_url_exception_handler, unauthorized_access_handler
from app.exceptions import InvalidUrlException, UnauthorizedAccessException
from app.schemas import ProfileListRequest, BulkProfilesRequest, PredictionResponse
from app.extractor import extract_features_from_instagram
from app.prediction_client import predict_profiles
from app.exceptions import GenericInternalException
from app.exception_handler import generic_internal_exception_handler
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Instagram Feature Extraction Service")
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set this to your React frontend URL like "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods like POST, GET, OPTIONS etc.
    allow_headers=["*"],
)

@app.post("/predict", response_model=PredictionResponse)
async def extract_profiles(request: ProfileListRequest):

    print("Signature",request.signature)
    print("Profile_Urls",request.profile_urls)

    message_string = ",".join(request.profile_urls)

    try:
        if not is_authorized(message_string,request.signature):
            raise UnauthorizedAccessException(
                code=ERRORS["UNAUTHORIZED_ACCESS"]["code"],
                message=ERRORS["UNAUTHORIZED_ACCESS"]["message"],
                details="Unauthorized Access Please use the valid API_SECRET_KEY"
            )

        # Validate the URLs first
        for url in request.profile_urls:
            if not url.startswith("https://www.instagram.com/"):
                logging.error(f"Invalid URL: {url}")
                raise InvalidUrlException(
                    code=ERRORS["INVALID_URL"]["code"],
                    message=ERRORS["INVALID_URL"]["message"],
                    details="Expected Instagram profile URL."
                )

        # Fetch features for all profiles in one batch (via Apify Actor)
        logging.info(f"Processing {len(request.profile_urls)} profiles...")

        features_list = await extract_features_from_instagram(request.profile_urls)

        # Send the features list to the prediction service
        prediction_request = BulkProfilesRequest(profiles=features_list)
        prediction_response = await predict_profiles(prediction_request)

        return prediction_response

    except UnauthorizedAccessException as e:
        raise e

    except GenericInternalException as e:
        raise e
    except InvalidUrlException as e:
        raise e

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing profiles.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

# Register custom exception handler
app.add_exception_handler(InvalidUrlException, invalid_url_exception_handler)
app.add_exception_handler(GenericInternalException, generic_internal_exception_handler)
app.add_exception_handler(UnauthorizedAccessException,unauthorized_access_handler)

