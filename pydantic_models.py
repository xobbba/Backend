from pydantic import BaseModel
from typing import Optional


class SignUp(BaseModel):
    full_name: str
    sex: str
    date_birth: str
    employer: bool
    login: str
    password: str
    skills: Optional[str] = None
    hobby: Optional[str] = None


class SignIn(BaseModel):
    login: str
    password: str


class LikeUser(BaseModel):
    id_user: int
    like: bool