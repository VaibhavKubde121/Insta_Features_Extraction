from fastapi import HTTPException

class InvalidUrlException(Exception):
    def __init__(self, code: int, message: str, details: str = None):
        self.code = code
        self.message = message
        self.details = details or "No additional details provided"



class GenericInternalException(HTTPException):
    def __init__(self, code: int, message: str, details: str = None):
        super().__init__(status_code=500, detail={
            "code": code,
            "message": message,
            "details": details
        })


class UnauthorizedAccessException(HTTPException):
    def __init__(self, code: int, message: str, details: str = None):
        super().__init__(status_code=401, detail={
            "code": code,
            "message": message,
            "details": details
        })