from fastapi import FastAPI, HTTPException
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from app.auth import is_authorized
from app.errors import ERRORS
from app.exception_handler import (
    invalid_url_exception_handler,
    unauthorized_access_handler,
    generic_internal_exception_handler,
)
from app.exceptions import (
    InvalidUrlException,
    UnauthorizedAccessException,
    GenericInternalException,
)
from app.schemas import (
    FeatureRequest,
    BulkProfilesRequest,
    SuccessResponse,
    PredictionResult, ProfileListRequest,
    # Add ProfileListRequest for incoming request structure
)
from app.extractor import extract_features_from_instagram
from app.prediction_client import predict_profiles
from app.config import PLATFORM_REF_INSTAGRAM  # should be defined as a constant

app = FastAPI(title="Instagram Feature Extraction Service")
logging.basicConfig(level=logging.INFO)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model=SuccessResponse)
async def extract_profiles(request: ProfileListRequest):
    message_string = ",".join(request.profile_urls)

    try:
        # Step 1: Signature Validation
        if not is_authorized(message_string, request.signature):
            raise UnauthorizedAccessException(
                code=ERRORS["UNAUTHORIZED_ACCESS"]["code"],
                message=ERRORS["UNAUTHORIZED_ACCESS"]["message"],
                details="Unauthorized Access: Invalid API_SECRET_KEY"
            )

        # Step 2: URL Validation
        for url in request.profile_urls:
            if not url.startswith("https://www.instagram.com/"):
                raise InvalidUrlException(
                    code=ERRORS["INVALID_URL"]["code"],
                    message=ERRORS["INVALID_URL"]["message"],
                    details="Expected an Instagram profile URL."
                )

        # Step 3: Extract Features
        extracted_profiles = await extract_features_from_instagram(request.profile_urls)


        # Step 5: Prepare Bulk Request for Prediction
        prediction_request = BulkProfilesRequest(profiles=extracted_profiles)

        # Step 6: Call Prediction Service
        prediction_response = await predict_profiles(prediction_request)

        # Step 7: Wrap response in SuccessResponse
        return SuccessResponse(
            status="success",
            code=200,
            message="Predictions generated successfully.",
            data=prediction_response.data  # This should contain the prediction results
        )

    except (UnauthorizedAccessException, InvalidUrlException, GenericInternalException) as e:
        raise e

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred during processing.")


# Register custom handlers for exceptions
app.add_exception_handler(InvalidUrlException, invalid_url_exception_handler)
app.add_exception_handler(GenericInternalException, generic_internal_exception_handler)
app.add_exception_handler(UnauthorizedAccessException, unauthorized_access_handler)

# Entry Point for Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)