"""
schemas/user.py
用户相关的数据模型
"""

from pydantic import  UUID4, EmailStr, constr
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class UserData(BaseModel):
    user_id: Optional[UUID] =Field(None,description="用户id")
    account: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[int] = None
    points: Optional[int] = None
    photo_url: Optional[str] = None
    invitation_code: Optional[str] = None
    identify: Optional[int] = None


class UserRegister(BaseModel):
    username: Optional[str] = Field(
        default=None,
        description="用户的用户名，可选"
    )
    phone: str = Field(
        ...,
        description="用户的手机号码或者账号必填",
        min_length=11,
        max_length=11
    )
    password: str = Field(
        ...,
        description="用户的密码，必填",
        min_length=6,
        max_length=20
    )
    verification_code: Optional[str]= Field(
        default=None,
        description="验证码，可选",
        min_length=4,
        max_length=6
    )
    invitation_code: Optional[str] = Field(
        default=None,
        description="邀请码，可选"
    )

    @field_validator('phone')
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("手机号码必须为数字")
        return value
    




class UserCodeLogin(BaseModel):
    phone: str
    code: str

class UserReset(BaseModel):
    phone: str
    password: str
    code: str

class UserPasswordLogin(BaseModel):
    account: str # 可能为手机号，也可能为账号
    password: str

class UserUpdate(BaseModel):
    account: Optional[str] = None
    username: Optional[str] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None

class UserResponse(BaseModel):
    user_id: UUID4
    account: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    points: Optional[int] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None
    photo_url: Optional[str] = None
    identify: int
    invitation_code: Optional[str] = None
