from fastapi import FastAPI, HTTPException, Depends

from backend.auth.auth_bearer import JWTBearer
from .routes.route_user import route_user

if __name__ == '__main__':
    app = FastAPI()

    app.include_router(route_user, prefix='/auth')

    # app.include_router(router, prefix='', dependencies=[Depends(JWTBearer())])