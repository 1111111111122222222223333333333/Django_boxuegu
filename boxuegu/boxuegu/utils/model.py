from django.db import models
import datetime
# 封装模型类中的共有时间，创建时间和修改时间，
# 这个模型类不需要创建表
class BaseModels(models.Model):
    # 自动添加时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 自动修改时间
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 当前类为抽象类，不需要表，只继承
        abstract = True