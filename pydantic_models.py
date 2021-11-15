from pydantic import BaseModel
from typing import Optional


class SignUp(BaseModel):
    full_name: str
    sex: str
    date_birth: str
    age: int
    employer: bool
    login: str
    password: str
    skills: Optional[str] = None
    hobby: Optional[str] = None


class SignIn(BaseModel):
    login: str
    password: str