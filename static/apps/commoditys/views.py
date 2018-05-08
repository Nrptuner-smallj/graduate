from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

from .models import Commodity
from opreation.models import LackCommodity


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

    def get(self,request):
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


