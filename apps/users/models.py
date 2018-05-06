from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name="用户名",  unique=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), null=True, blank=True, verbose_name="性别",
                              max_length=8, default='male')
    tel = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    paypass = models.CharField(max_length=6,null=True,blank=True,verbose_name="支付密码")
    wallet = models.FloatField(default=500, verbose_name="账户余额")

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class EmailCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=30, verbose_name="发送对象")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")
    send_type = models.CharField(choices=(('register', '注册'),('forgetpwd','忘记密码')), verbose_name="用途", max_length=20)

    class Meta:
        verbose_name = "邮箱验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}+{}'.format(self.email, self.get_send_type_display())
