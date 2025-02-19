"""
user.py
存放用户相关接口，如登录注册修改信息等
"""

from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from app.models.user import User
from app.schemas.response import ResponseModel
from app.schemas.user import UserRegister,UserPasswordLogin,UserUpdate,UserCodeLogin
from app.utils.user import create_jwt
from app.utils.user.user_function import redis_client,map_user_to_user_response,get_current_user, get_code, check_code,generate_account
from app.utils.database.redis import get_redis
from app.utils.secure import md5
from app.config.constant import *


# 生成路由对象
api_user = APIRouter()

redis = get_redis()



#用户注册部分 /register开头


@api_user.post("/register",description="用户注册")
async def register(user_register: UserRegister):
    username = user_register.username
    phone = user_register.phone
    password = user_register.password
    code =  user_register.code
    invitation_code = user_register.invitation_code

    # 检查信息是否为空
    if not phone:
        raise HTTPException(status_code=400, detail="手机号不得为空！")
    if not code:
        raise HTTPException(status_code=400, detail="验证码不得为空！")
    if not password:
        raise HTTPException(status_code=400, detail="密码不得为空！")
    if not username:
        username = "用户" + str(phone)

    # 校验手机号与验证码是否合法
    await check_code(code, phone, REDIS_USER_REGISTER_CODE)
    # 查找用户
    user = await User.filter(phone = phone).first()
    # 用户存在
    if user:
        token = create_jwt(user)
        return ResponseModel.success("用户已存在，已登录", {"current_user" : get_current_user(token), "token" : token})
    else:
        # 用户不存在，创建新用户并直接登录

        # 查看邀请码对应的用户
        # 两个人都加积分，各加 1000 分
        # todo 区分一级还是二级代理商
        add_points = 1000
        inviting_user = await User.filter(invitation_code=invitation_code).first()
        # 邀请码有效
        if inviting_user:
            user_id = inviting_user.user_id
            old_points = inviting_user.points
            result = await User.filter(user_id=user_id).update(points=add_points + old_points)

        # 有邀请码，两个人都额外加 1000 分
        add_points = add_points + 1000

        try:
            newUser = await User.create(
                account = generate_account(),
                phone = phone,
                username = username,
                password = md5(password),
                points = add_points
            )

            # 生成 token
            token = create_jwt(newUser)
            return ResponseModel.success("注册用户成功", {"current_user" : get_current_user(token), "token" : token})
        except IntegrityError:
            raise HTTPException(status_code=500, detail="用户创建失败，请稍后重试")
        
#用户登录部分 /login开头

@api_user.get("/login_send_verification_code", description="发送登录账号时候需要的验证码")
async def login_send_verification_code(phone : str):
    code = await get_code(phone, REDIS_USER_LOGIN_CODE)
    return ResponseModel.success("登录账号验证码发送成功")


@api_user.post("/login_verification_code",description="手机号验证码登录")
async def login_verification_code(user_login: UserCodeLogin):
    phone = user_login.phone
    code = user_login.code
    # 校验
    if not phone or not code:
        raise HTTPException(status_code=400, detail="手机号或验证码不能为空！")
    # 数据库查询

    # 查询用户
    user = await User.filter(phone = phone).first()
    if user is None:
        raise HTTPException(status_code=400, detail="用户不存在！")
    await check_code(code, phone, REDIS_USER_LOGIN_CODE)

    # 生成 token
    token = create_jwt(user)

    # 使用 UserResponse 映射并返回
    user_data = map_user_to_user_response(user)

    return ResponseModel.success("登录成功", {"token": token, "user": user_data})


@api_user.post("/login_password",description="账号密码登录（输入手机号和账号均可）")
async def login_password(user_login: UserPasswordLogin):
    account = user_login.account # 可能为账号，可能为手机号
    password = user_login.password
    # 校验
    if not account or not password:
        raise HTTPException(status_code=400, detail="账号或密码不能为空！")
    # 数据库查询
    # 数据库查询，使用 Q 进行联合查询（账号或手机号）
    user = await User.filter(Q(account=account) | Q(phone=account)).first()
    if user is None:
        raise HTTPException(status_code=400, detail="用户不存在！")

    # 验证密码
    if user.password != md5(password):
        raise HTTPException(status_code=400, detail="账号或密码错误！")

    # 生成 token
    token = create_jwt(user)

    # 使用 UserResponse 映射并返回
    user_data = map_user_to_user_response(user)

    return ResponseModel.success("登录成功", {"token": token, "user": user_data})


@api_user.post("/logout", description="退出登录")
async def logout(token : str):
    redis_client.set(token, "expired", ex=2592000) # 单位: 秒 - > 一个月

    return ResponseModel.success("注销成功")


#用户重置部分 /reset开头
@api_user.get("/reset_password_send_verification_code", description="发送找回（重置）密码的验证码")
async def reset_password_send_verification_code(phone : str):
    code = await get_code(phone, REDIS_USER_RESET_CODE)
    return ResponseModel.success("找回密码验证码发送成功")

@api_user.post("/reset_information", description="修改用户信息，注意，不需要修改的字段无需传入；修改后的token会重新生成")
async def reset_information(user_update: UserUpdate,token: str):
    current_user = get_current_user(token)
    """
    修改用户信息接口：
    1. 修改自己的信息。
    2. 禁止修改不可更新的字段
    UserUpdate 字段
    account,username,gender,email
    """
    user_id = current_user.user_id

    account = user_update.account
    username = user_update.username
    gender = user_update.gender
    email = user_update.email

    # 查找原用户
    original_user = await User.filter(user_id=user_id).first()
    if not original_user:
        raise HTTPException(status_code=403, detail="用户不存在，操作非法")

    if username is None:
        username = original_user.username
    if account is None:
        account = original_user.account
    if gender is None:
        gender = original_user.gender
    if email is None:
        email = original_user.email

    # 更新数据库
    await User.filter(user_id = user_id).update(
            account = account,
            username = username,
            gender = gender,
            email = email
    )
    updated_user = await User.filter(user_id=user_id).first()
    token = create_jwt(updated_user)
    updated_user = map_user_to_user_response(updated_user)

    return ResponseModel.success("修改个人信息成功", {"token": token, "updated_user": updated_user})

#用户查看部分 /get开头
@api_user.get("/get_profile", description="查看当前用户信息")
async def get_profile(token: str):
    current_user = get_current_user(token)

    return ResponseModel.success("获取当前用户信息成功", {"current_user": current_user})

@api_user.get("/get_profile_photo", description="获取个人头像(地址)")
async def get_profile_photo(token: str):
    current_user = get_current_user(token)
    user = await User.filter(user_id=current_user.user_id).first()
    return ResponseModel.success("获取当前用户头像地址成功", {"photo_url": current_user.photo_url})


@api_user.get("/get_all_users", description="查询全部用户")
async def get_all_users(token: str):
    current_user = get_current_user(token)

    if current_user.identify != ADMIN_ROLE:
        raise HTTPException(status_code=403, detail="无管理员权限！")
    user_list = await User.filter().all()

    # 通过返回精简后的字段
    return ResponseModel.success("查询全部用户信息成功",{"user_list" : [map_user_to_user_response(user) for user in user_list]})


