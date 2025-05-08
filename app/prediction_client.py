from http.client import HTTPException

import httpx
import logging
from app.config import PREDICTION_SERVICE_URL
from app.errors import ERRORS
from app.exceptions import GenericInternalException
from app.schemas import BulkProfilesRequest, PredictionResponse

logging.basicConfig(level=logging.INFO)

async def predict_profiles(request_data: BulkProfilesRequest) -> PredictionResponse:
    url = f"{PREDICTION_SERVICE_URL}/predict-profiles"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=request_data.dict())
            response.raise_for_status()
            return PredictionResponse(**response.json())

    except httpx.HTTPStatusError as e:
        logging.error(f"Prediction service returned an error: {e.response.status_code} - {e.response.text}")
        raise GenericInternalException(
            code=ERRORS["INTERNAL_ERROR"]["code"],
            message=ERRORS["INTERNAL_ERROR"]["message"],
            details=f"Prediction service failed with status {e.response.status_code}"
        )

    except httpx.RequestError as e:
        logging.error(f"Request error while calling prediction service: {str(e)}")
        raise GenericInternalException(
            code=ERRORS["INTERNAL_ERROR"]["code"],
            message=ERRORS["INTERNAL_ERROR"]["message"],
            details="Prediction service is unreachable."
        )

    except Exception as e:
        logging.error(f"Unexpected error while calling prediction service: {str(e)}")
        raise GenericInternalException(
            code=ERRORS["INTERNAL_ERROR"]["code"],
            message=ERRORS["INTERNAL_ERROR"]["message"],
            details="Something went wrong while communicating with prediction service."
        )