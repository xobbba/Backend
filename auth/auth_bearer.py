from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_hadler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(
                    status_code=403,
                    detail='Неверная схема аутентификации'
                )

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail='Неверный токен или токен с истекшим сроком действия'
                )

            return credentials.credentials

        else:
            raise HTTPException(
                status_code=403,
                detail='Неверный код авторизации.'
            )

    def verify_jwt(self, jwtoken):

        isTokenValid = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid
