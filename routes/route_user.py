from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from pydantic_models import SignUp, SignIn
from models import Session, User
from fastapi import HTTPException, APIRouter
from auth.auth_hadler import signJWT
import bcrypt

BCRYPT_SALT = b'$2b$12$o2rj9W4ToE/NRwb1vIit9.'

route_user = APIRouter()


@route_user.post('/signup')
async def signup(q: SignUp):
    try:
        user = Session().query(User).filter_by(login=q.login).first()
        if user is not None:
            raise HTTPException(status_code=400,
                                detail='Пользователь с таким логином уже существует')  # посмотреть код ошибки
        new_user = User(full_name=q.full_name,
                        sex=q.sex,
                        date_birth=parser.parse(q.date_birth).date(),
                        age=int(relativedelta(datetime.now().date(), parser.parse(q.date_birth).date()).years),
                        employer=q.employer,
                        login=q.login,
                        password=bcrypt.hashpw(q.password.encode(), BCRYPT_SALT),
                        skills=q.skills,
                        hobby=q.hobby)

        s = Session()
        s.add(new_user)
        s.commit()

        return 'OK'
    except Exception as ex:
        raise HTTPException(status_code=501)


@route_user.post('/signin')
async def signin(q: SignIn):
    try:
        user = Session().query(User).filter_by(login=q.login).first()
        if user is None:
            raise HTTPException(status_code=401, detail='Пользователя с таким логином не существует')  # посмотреть код ошибки
        if bcrypt.hashpw(q.password.encode(), BCRYPT_SALT) == user.password:
            raise HTTPException(status_code=401,
                                detail='Неверный пароль.')
        return {'token': signJWT(user.login, user.employer, user.id)}
    except Exception as ex:
        return {
                    'error': ex
                }
