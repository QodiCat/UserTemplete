"""
user.py
存放用户相关接口，如登录注册修改信息等
"""

from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from app import redis_client
from app.models.user import User
from app.schemas.response import ResponseModel
from app.schemas.user import UserRegister,UserPasswordLogin,UserUpdate,UserCodeLogin
from app.utils.user import create_jwt,map_user_to_user_response,get_current_user, get_code, check_code,generate_account,md5



# 生成路由对象
api_user = APIRouter(prefix="/user", tags=["用户相关接口"])

#用户注册部分,有两种注册方式，一种是手机号+密码，一种是手机号+验证码




