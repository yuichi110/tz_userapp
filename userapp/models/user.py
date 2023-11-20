from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str


class UserSchemaWithoutPassword(BaseModel):
    id: str
    username: str
    email: str


class SignupBody(BaseModel):
    username: str
    email: str
    password1: str
    password2: str


class SigninBody(BaseModel):
    username_or_email: str
    password: str
