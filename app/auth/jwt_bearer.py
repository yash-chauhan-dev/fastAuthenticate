# The function of this file is to check whether the request is
# authorized or not [Verication of the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid or Expired token!")
            jwt_verified = self.verify_jwt(credentials.credentials)
            if jwt_verified:
                return credentials.credentials
            else:
                raise HTTPException(
                    status_code=403, detail="Invalid or Expired token!")
        else:
            raise HTTPException(
                status_code=403, detail="Invalid or Expired token!")

    def verify_jwt(self, jwttoken: str):
        isTokenValid: bool = False
        payload = decodeJWT(jwttoken)
        if payload:
            isTokenValid = True
        return isTokenValid
