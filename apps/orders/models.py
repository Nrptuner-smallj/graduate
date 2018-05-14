from datetime import datetime
from django.db import models

from users.models import UserProfile
from commoditys.models import Commodity
from users.models import Address

# Create your models here.

class Order(models.Model):

    id = models.CharField(max_length=25,verbose_name="订单编号",primary_key=True)
    user = models.ForeignKey(UserProfile,verbose_name="下单用户",on_delete=models.CASCADE)
    status = models.CharField(choices=(('unpaid','未付款'),('paid','已支付'),('fininshed','已完成')),max_length=11,verbose_name="订单状态");
    total_price = models.FloatField(verbose_name="订单总价")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="创建时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def get_delivery(self):
        return self.deliveryorder_set.all()

    def __str__(self):
        return self.id

    def isallout(self):
        for delivery in self.get_delivery().all():
            if delivery.status == 'ing':
                return False
        return True

class DeliveryOrder(models.Model):
    id = models.CharField(max_length=26,verbose_name="出货单号",primary_key=True)
    address = models.CharField(max_length=200,verbose_name="收货信息",null=True,blank=True)
    order = models.ForeignKey(Order,verbose_name="所属订单",on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity,verbose_name="商品",on_delete=models.CASCADE)
    nums = models.IntegerField(default=1,verbose_name="购买数量")
    status = models.CharField(choices=(('ing','出货中'),('ed','已出货')),max_length=5,verbose_name="出货情况")
    tracking = models.CharField(max_length=16,verbose_name='快递单号',null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "出货单"
        verbose_name = verbose_name_plural

    def get_totalprice(self):
        return self.commodity.price*self.nums

    def __str__(self):
        return self.id


class ReturnOrder(models.Model):
    id = models.CharField(max_length=26,verbose_name="退单号",primary_key=True)
    type = models.CharField(choices=(('m','仅退款'),('mc','退货与款')),default='m',max_length=10)
    delivery = models.ForeignKey(DeliveryOrder,verbose_name="出货单",on_delete=models.CASCADE)
    status = models.CharField(choices=(('accept','同意退货'),('reject','拒绝退款')),verbose_name="退货审核",max_length=7)
    reason = models.CharField(max_length=100,verbose_name="退货原因",null=True,blank=True)
    return_status = models.CharField(choices=(('un','未退回'),('ing','已退回'),('ed','已退货')),max_length=6,null=True,blank=True)
    return_tracking = models.CharField(max_length=16,verbose_name='退货快递单号',null=True,blank=True)

    class Meta:
        verbose_name_plural = "退货单"
        verbose_name = "退货单"

    def __str__(self):
        return self.id