from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(UserSchema):
    id: str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    email:str