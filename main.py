from fastapi import Depends, FastAPI

from auth.auth_bearer import JWTBearer
from routes.route_user import route_user
from routes.router_list import router_list

app = FastAPI()

app.include_router(route_user, prefix='/auth')
app.include_router(router_list, prefix='/like_list', dependencies=[Depends(JWTBearer())])

# app.include_router(router, prefix='', dependencies=[Depends(JWTBearer())])
