"""
schemas/user.py
用户相关的数据模型
"""

from pydantic import BaseModel, UUID4
from typing import Optional
from uuid import UUID
from pydantic.fields import Field


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
    username: str
    phone: str
    password: str
    code: str                   # 验证码
    invitation_code: Optional[str] = None # 邀请码，可选择

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
