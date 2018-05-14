import time
import random

from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from django.contrib.auth.hashers import make_password, check_password

from .models import Commodity
from opreation.models import LackCommodity, ShopCartRecord,UserComment
from orders.models import Order, DeliveryOrder


# Create your views here.

class SearchView(View):

    def get(self, request):
        key_word = request.GET.get("keywords")
        commoditys = Commodity.objects.filter(
            Q(name__icontains=key_word) | Q(author=key_word) | Q(publisher=key_word) | Q(
                catagory__name__icontains=key_word) | Q(catagory__cata_up__name__icontains=key_word) | Q(
                desc__icontains=key_word))
        nums = commoditys.count()
        rank_commoditys = commoditys.order_by('click_nums')[:5]
        # 进行排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "price":
                commoditys = commoditys.order_by("-price")
            elif sort == "sell_nums":
                commoditys = commoditys.order_by("-sell_nums")
            elif sort == "click_nums":
                commoditys = commoditys.order_by("-click_nums")
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(commoditys, 20, request=request)

        commoditys = p.page(page)

        return render(request, "commoditylist.html",
                      dict(commoditys=commoditys, key_word=key_word, nums=nums, rank_commoditys=rank_commoditys,
                           sort=sort))


class DetailView(View):
    """书本细节"""

    def get(self, request, commodity_id):
        commodity = Commodity.objects.get(id=commodity_id)
        recommend = Commodity.objects.filter(catagory=commodity.catagory)[:5]
        could_buy = 0
        if commodity.stock == 0:
            could_buy = 1
        if request.user.is_authenticated:
            if request.user.paypass == '':
                could_buy = 1
        desc = commodity.desc.replace('<br/><br/>', '\n').replace('<br/>', '')
        catalog = commodity.catalog.replace('<br/>', '').replace('<div id="ml_txt" style="display:none;">', '')
        return render(request, "commditydetail.html",
                      dict(commodity=commodity, could_buy=could_buy, desc=desc, catalog=catalog, recommend=recommend))


class LackView(View):
    """缺货登记"""

    def get(self, request):
        name = request.GET.get("name")
        bookurl = request.GET.get("bookurl")
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        lack_record = LackCommodity()
        lack_record.name = name
        lack_record.url = bookurl
        lack_record.user = request.user
        lack_record.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class AddToShopCart(View):
    """添加购物车"""

    def get(self, request):
        try:
            commodity_id = request.GET.get("id")
            count = request.GET.get("count")
            commodity = Commodity.objects.get(id=commodity_id)
            if ShopCartRecord.objects.filter(user=request.user, commodity=commodity):
                record = ShopCartRecord.objects.get(user=request.user, commodity=commodity)
                if commodity.stock < record.nums + int(count):
                    return HttpResponse('{"status":"fail"}', content_type='application/json')
                else:
                    record.nums = record.nums + int(count)
                    record.save()
                    return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                record = ShopCartRecord();
                record.user = request.user
                record.commodity = commodity
                record.nums = count
                record.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        except:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ToConfirmView(View):
    """购买跳转"""

    def get(self, request):
        items = request.GET.getlist('items[]')
        ids = []
        for item in items:
            ids.append(int(item))
        records = ShopCartRecord.objects.filter(id__in=items)
        if_lack = 1
        for record in records:
            if record.nums > record.commodity.stock:
                if_lack = 0
        if if_lack == 0:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class ConfirmInfoView(View):
    """购买信息确认"""

    def get(self, request):
        items = request.GET.getlist('items')
        ids = []
        for item in str(items).replace('[', '').replace(']', '').replace("'", "").split(','):
            ids.append(int(item))
        records = ShopCartRecord.objects.filter(id__in=ids)
        addresses = request.user.address_set.all()
        return render(request, 'informationconfirm.html', dict(records=records, addresses=addresses))


class PayView(View):
    """购买逻辑处理"""

    def get(self, request):
        ids = request.GET.getlist('record_id')
        address = request.GET.get('address')
        new_ids = []
        for id in ids:
            new_ids.append(int(id))
        total_price = 0.0
        records = ShopCartRecord.objects.filter(id__in=new_ids)

        # 创建订单
        for record in records:
            total_price = total_price + (record.nums * record.commodity.price)
        order = Order()
        # 订单总价
        order.total_price = total_price
        # 订单状态
        order.status = 'unpaid'
        # 用户
        order.user = request.user
        # 唯一的订单号生成 时间戳+四位随机数+用户四位标识符
        t = time.time()
        timestamp = str(round(t * 1000))
        ran = random.randint(1, 9999)
        id = ''
        while True:
            if request.user.id < 10000:
                id = 'D' + str(int(timestamp) * 100000000 + ran * 10000 + request.user.id)
            else:
                id = 'D' + str(int(timestamp) * 100000000 + ran * 10000 + int(str(request.user.id))[-5:-1])
            if not Order.objects.filter(id=id):
                break
        order.id = id
        order.save()
        # 分别创建发货单
        for i, record in enumerate(records):
            delivery_order = DeliveryOrder()
            delivery_order.id = order.id.replace('D', 'C') + str(i)
            delivery_order.address = address
            delivery_order.order = order
            delivery_order.commodity = record.commodity
            delivery_order.nums = record.nums
            delivery_order.status = 'ing'
            delivery_order.tracking = ''
            delivery_order.save()

        # 删去购物车的记录
        l = len(records)
        records.delete()
        return render(request, 'pay.html', dict(order=order))

    def post(self, request):
        # 支付操作
        order_id = request.POST.get('order_id')
        paypwd = request.POST.get('paypwd')

        order = Order.objects.get(id=order_id)
        user = request.user
        # 检查支付密码
        if not check_password(paypwd, request.user.paypass):
            return render(request, "pay.html", dict(order=order, msg='支付密码错误'))
        # 检查余额是否充足
        if user.wallet < order.total_price:
            return render(request, "pay.html", dict(order=order, msg='钱包余额不足'))
        # 检查订单内是否所有货物充足
        for delivery in order.get_delivery():
            if delivery.nums > delivery.commodity.stock:
                return render(request, "pay.html", dict(order=order, msg='《' + delivery.commodity.name + '》' + '货源不足'))

        # 将商品库存数量减一
        for delivery in order.get_delivery():
            commodity = delivery.commodity
            commodity.stock = commodity.stock - delivery.nums
            commodity.save()
        user.wallet = user.wallet - order.total_price
        user.save()
        order.status = 'paid'
        order.save()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('users:paidorder'))


class AddCommentView(View):
    """商品评论"""

    def get(self, request,commodity_id):
        commodity = Commodity.objects.get(id=commodity_id)
        recommend = Commodity.objects.filter(catagory=commodity.catagory)[:5]
        could_buy = 0
        if commodity.stock == 0:
            could_buy = 1
        if request.user.is_authenticated:
            if request.user.paypass == '':
                could_buy = 1
        comments = UserComment.objects.filter(commodity=commodity)
        return render(request,"commditycomment.html",dict(commodity=commodity,recommend=recommend,could_buy=could_buy,comments=comments))
