from sqlalchemy import select
from pydantic_models import LikeUser
from models import User, LikeUsersList, Session, engine
from fastapi import HTTPException, APIRouter, Cookie, Depends, Request
from auth.auth_hadler import JWTtoJSON

router_list = APIRouter()


@router_list.post('/likeUser')
def like_user_list(q: LikeUser, request: Request):
    thisUser = JWTtoJSON(request.headers['authorization'][7:])

    if q.id_user == thisUser['id']:
        raise HTTPException(status_code=501, detail="Себя лайкать нельзя :3")

    if not thisUser['employer']:
        raise HTTPException(status_code=403, detail="Только работодатель может лайкать")

    try:
        user = Session().query(User).filter_by(id=q.id_user).first()
        if user and not user.employer:git
            tmp = Session().query(LikeUsersList).filter_by(id_employer=thisUser['id'],
                                                           id_user=q.id_user).first()
            if tmp:
                raise HTTPException(status_code=401, detail="one like to user")

            like = LikeUsersList(
                id_employer=thisUser['id'],
                id_user=user.id,
                like=q.like
            )
            s = Session()
            s.add(like)
            s.commit()

            return 'OK'
        raise HTTPException(status_code=401, detail="User cannot be liked")
    except Exception as ex:
        raise HTTPException(status_code=501, detail="Server Error")


@router_list.get('/userLikes')  # просмотр поставленных собой лайков
def userLikes(request: Request):
    thisUser = JWTtoJSON(request.headers['authorization'][7:])

    try:
        select_user_like = select(LikeUsersList.id_user, LikeUsersList.like).filter_by(id_employer=thisUser['id'])
        likes = Session().execute(select_user_like).all()
        if likes:
            return likes
        raise HTTPException(status_code=401, detail="Not likes")
    except Exception as ex:
        raise HTTPException(status_code=501, detail="Server Error")
