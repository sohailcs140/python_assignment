from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(UserSchema):
    id: str
