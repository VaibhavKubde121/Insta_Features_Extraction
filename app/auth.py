import hmac
import hashlib

API_SECRET_KEY = "B7@dX#9Kq$1m^tFW!ZgL&pY82uERvj5A*hM0Nc!xoQz4UVSfb6TLkwC#iD3n%JM"

def generate_signature(message: str) -> str:
    return hmac.new(API_SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()

def is_authorized(message: str, received_signature: str) -> bool:
    expected_signature = generate_signature(message)
    print("Expected Signature : ", expected_signature)
    print("Received Signature : ", received_signature)
    return hmac.compare_digest(expected_signature, received_signature)