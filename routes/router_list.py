from sqlalchemy import select, delete, update, insert
from pydantic_models import LikeUser
from models import User, LikeUsersList, Session, engine
from fastapi import HTTPException, APIRouter, Cookie, Depends, Request
from auth.auth_hadler import JWTtoJSON

router_list = APIRouter()


@router_list.post('/likeUser', summary='Adds a like to the user. You can change the values')
def like_user_list(q: LikeUser, request: Request):
    thisUser = JWTtoJSON(request.headers['authorization'][7:])

    if q.id_user == thisUser['id']:
        raise HTTPException(status_code=501, detail="Себя лайкать нельзя :3")

    if not thisUser['employer']:
        raise HTTPException(status_code=403, detail="Только работодатель может лайкать")

    user = Session().query(User).filter_by(id=q.id_user).first()

    if not user or user.employer:
        raise HTTPException(status_code=401, detail="User cannot be liked")

    s = Session()
    tmp = s.query(LikeUsersList).filter_by(id_employer=thisUser['id'],
                                           id_user=q.id_user).first()

    if tmp and tmp.like == q.like:
        delete_like = delete(LikeUsersList).filter_by(id_user=tmp.id_user)
        s.execute(delete_like)
        s.commit()
        return "OK"

    elif tmp and tmp.like != q.like:
        tmp.like = not tmp.like

        s.add(tmp)
        s.commit()
        return 'OK'

    like = LikeUsersList(
        id_employer=thisUser['id'],
        id_user=user.id,
        like=q.like
    )
    s.add(like)
    s.commit()

    return "OK"


@router_list.get('/userLikes', summary='Conclusion of liked users')
def userLikes(request: Request):
    thisUser = JWTtoJSON(request.headers['authorization'][7:])

    select_user_like = select(LikeUsersList.id_user, LikeUsersList.like).filter_by(id_employer=thisUser['id'])
    likes = Session().execute(select_user_like).all()
    if likes:
        return likes
    raise HTTPException(status_code=401, detail="Not likes")
