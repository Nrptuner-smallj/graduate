from datetime import datetime

from django.db import models
from users.models import UserProfile

# Create your models here.

class LackCommodity(models.Model):

    name = models.CharField(max_length=50,verbose_name="书名")
    url = models.CharField(max_length=100,verbose_name="链接")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="填写时间")
    user = models.ForeignKey(UserProfile,verbose_name="登记用户",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "缺货登记"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
