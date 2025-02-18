
import string
import secrets

def generate_invitation_code(length=6):
    # 使用 secrets 生成一个包含字母和数字的随机字符串
    characters = string.ascii_letters + string.digits  # 可以根据需要增加字符集
    digits = string.digits
    return ''.join(secrets.choice(digits) for i in range(length))