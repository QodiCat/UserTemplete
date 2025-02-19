
import uuid
import string
import secrets
from tortoise.models import Model
from tortoise import fields
from ..utils.user import generate_invitation_code

class User(Model):
    user_id = fields.UUIDField(pk=True, default=uuid.uuid4, index=True)
    phone = fields.CharField(default="", max_length=100, description="电话号")
    account = fields.CharField(default="", max_length=100, description="账户")# 往往和phone相同
    username = fields.CharField(default="", max_length=100, description="用户名")
    password = fields.CharField(default="", max_length=100, description="密码")

    



