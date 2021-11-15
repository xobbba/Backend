from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from ..pydantic_models import SignUp, SignIn
from ..models import engine, Session, User
from ..main import app
from fastapi import HTTPException


@app.post('/signup')
async def signup(q: SignUp):
    try:
        user = Session().query(User).filter_by(login=q.login).first()
        if user is not None:
            raise HTTPException(status_code=401,
                                detail='Пользователь с таким логином уже существует')  # посмотреть код ошибки
        new_user = User(full_name=q.full_name,
                        sex=q.sex,
                        date_birth=parser.parse(q.date_birth).date(),
                        age=int(relativedelta(datetime.now().date(), parser.parse(q.date_birth).date()).years),
                        employer=q.employer,
                        login=q.login,
                        password=q.password,
                        skills=q.skills,
                        hobby=q.hobby)

        s = Session()
        s.add(new_user)
        s.commit()

        return 'OK'
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=501)


@app.post('/signin')
async def signin(q: SignIn):
    try:
        user = Session().query(User).filter_by(login=q.login).first()
        if user is None:
            raise HTTPException(status_code=401,
                                detail='Пользователя с таким логином не существует')  # посмотреть код ошибки
        if user.password != q.password:
            raise HTTPException(status_code=401,
                                detail='Неверный пароль.')
        return 'OK'
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=501)
