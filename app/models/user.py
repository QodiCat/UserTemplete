
import uuid
import string
import secrets
from tortoise.models import Model
from tortoise import fields
from ..utils.user import generate_invitation_code

class User(Model):
    user_id = fields.UUIDField(pk=True, default=uuid.uuid4, index=True)
    account = fields.CharField(default="", max_length=100, description="账户")
    username = fields.CharField(default="", max_length=100, description="名称")
    password = fields.CharField(default="", max_length=100, description="密码")
    phone = fields.CharField(default="", max_length=100, description="电话号")
    email = fields.CharField(default="", max_length=100)
    gender = fields.SmallIntField(default=0, description="0 为男，1 为女")
    points = fields.BigIntField(default=0, description="积分")
    photo_url = fields.CharField(default="", max_length=100, description="头像的url(地址)")
    invitation_code = fields.CharField(max_length=30, default=generate_invitation_code, description="邀请码")
    identify = fields.SmallIntField(default=0, description="0-普通用户，1-一级代理商，2-二级代理商，3-管理员")


