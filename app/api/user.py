"""
user.py
存放用户相关接口，如登录注册修改信息等
"""

from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from app.config.constant import *
from app import redis_client,app_config,logger
from app.models.user import User
from app.schemas.response import ResponseModel
from app.schemas.user import UserRegister,UserPasswordLogin,UserUpdate,UserCodeLogin
from app.utils.user import create_jwt,get_current_user, get_code, check_code,generate_account,md5


def get_user_by_phone(phone):
    return User.filter(phone = phone).first()


api_user = APIRouter()



#------------------------------
#用户注册部分,有两种注册方式，一种是手机号+密码，一种是手机号+验证码
#------------------------------

@api_user.get("/register/verification-code/send",description="发送注册验证码")
async def register_verification_code_get(phone : str):
    REDIS_USER_REGISTER_CODE = app_config.redis_config["user_register_code"]
    await get_code(phone, REDIS_USER_REGISTER_CODE)
    return ResponseModel.success("注册账号验证码发送成功")


@api_user.post("/register/verification-code-way",description="通过验证码的方式进行用户注册")
async def register_by_verification_code(user_register: UserRegister):
    username = user_register.username
    phone = user_register.phone
    password = user_register.password
    verification_code =  user_register.verification_code
    invitation_code = user_register.invitation_code

    user_config=app_config["user_config"]
    init_points = user_config["user_points"]["init_points"]
    add_points = user_config["user_points"]["invite_points"]

    if not username:
        username = "用户" + str(phone)
    if verification_code:
        await check_code(verification_code, phone, REDIS_USER_REGISTER_CODE)
    user = await User.filter(phone = phone).first()

    if user:
        token = create_jwt(user)
        return ResponseModel.success("用户已存在，已登录", {"current_user" : get_current_user(token), "token" : token})
    else:
        # 用户不存在，创建新用户并直接登录,两者邀请加积分
        inviting_user = await User.filter(invitation_code=invitation_code).first()
        if inviting_user:
            inviting_user_old_points = inviting_user.points
            inviting_user.points=add_points + inviting_user_old_points
            await inviting_user.save()
        new_user_points = add_points+init_points
        # 新建用户
        try:
            newUser = await User.create(
                account = phone,
                phone = phone,
                username = username,
                password = md5(password),
                points = new_user_points
            )
            token = create_jwt(newUser)
            return ResponseModel.success("注册用户成功", {"current_user" : get_current_user(token), "token" : token})
        except IntegrityError:
            raise HTTPException(status_code=500, detail="用户创建失败，请稍后重试")
        

