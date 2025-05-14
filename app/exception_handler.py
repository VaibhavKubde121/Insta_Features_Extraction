from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import InvalidUrlException, UnauthorizedAccessException
from app.exceptions import GenericInternalException


async def invalid_url_exception_handler(request: Request, exc: InvalidUrlException):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    )

async def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

async def generic_internal_exception_handler(request: Request, exc: GenericInternalException):
    return JSONResponse(
        status_code=500,
        content={
            "code": exc.detail["code"],
            "message": exc.detail["message"],
            "details": exc.detail.get("details", None)
        }
    )
