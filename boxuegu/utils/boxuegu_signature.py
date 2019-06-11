from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


# 加密
def dumps(json, expires):
    # 1创建工具对象
    serializer = Serializer(settings.SECRET_KEY, expires)
    # 2加密
    s1 = serializer.dumps(json)
    # 3转字符串，返回
    return s1.decode()


# 解密
def loads(s1, expires):
    # 1创建工具对象
    serializer = Serializer(settings.SECRET_KEY, expires)
    try:
        # 2解密
        json = serializer.loads(s1)
    except:
        return None
    return json
